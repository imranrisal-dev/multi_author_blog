from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from .models import Post, Category, Tag, Comment, Like
from .forms import PostForm, CommentForm

# Custom decorator to check if user is Author
def author_required(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.is_author:
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied("You are not authorized to access this page.")
    return wrap

# 1. Homepage / Post Listing Page
def post_list(request):
    posts = Post.objects.filter(status='Published').order_by('-created_at')
    
    # Filter by Category
    category_slug = request.GET.get('category')
    if category_slug:
        posts = posts.filter(category__id=category_slug)

    # Filter by Tag
    tag_id = request.GET.get('tag')
    if tag_id:
        posts = posts.filter(tags__id=tag_id)

    # Search (Title or Content)
    query = request.GET.get('q')
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))

    # Pagination (5 posts per page)
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    tags = Tag.objects.all()

    return render(request, 'blog/post_list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'tags': tags,
    })

# 2. Post Detail Page
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    # Draft protection
    if post.status == 'Draft':
        if not request.user.is_authenticated or (request.user != post.author and not request.user.is_superuser):
            raise PermissionDenied

    # Increment view count safely using F() expression and session check
    session_key = f"viewed_post_{post.id}"
    if not request.session.get(session_key, False):
        Post.objects.filter(pk=post.pk).update(view_count=F('view_count') + 1)
        post.refresh_from_db()
        request.session[session_key] = True

    comments = post.comments.all()
    comment_form = CommentForm()

    user_has_liked = False
    if request.user.is_authenticated:
        user_has_liked = Like.objects.filter(post=post, user=request.user).exists()

    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post_detail', slug=post.slug)

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'user_has_liked': user_has_liked,
    })

# 3. Like/Unlike Toggle
@login_required
def like_toggle(request, slug):
    post = get_object_or_404(Post, slug=slug)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete() # Unlike if already liked
    return redirect('post_detail', slug=post.slug)

# 4. Delete Comment
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    # Allowed for Comment Owner, Post Owner, or Admin
    if request.user == comment.user or request.user == comment.post.author or request.user.is_superuser:
        post_slug = comment.post.slug
        comment.delete()
        return redirect('post_detail', slug=post_slug)
    else:
        raise PermissionDenied

# 5. Author Dashboard
@login_required
@author_required
def author_dashboard(request):
    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'blog/author_dashboard.html', {'posts': posts})

# 6. Create Post
@login_required
@author_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('author_dashboard')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form, 'title': 'Create Post'})

# 7. Edit Post
@login_required
@author_required
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user:
        raise PermissionDenied("You can only edit your own posts.")
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('author_dashboard')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form, 'title': 'Edit Post'})

# 8. Delete Post
@login_required
@author_required
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user:
        raise PermissionDenied("You can only delete your own posts.")
    
    if request.method == 'POST':
        post.delete()
        return redirect('author_dashboard')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

# 9. Public Author Profile Page
def author_profile(request, username):
    author_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=author_user, status='Published').order_by('-created_at')
    return render(request, 'blog/author_profile.html', {'author_user': author_user, 'posts': posts})