from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    STATUS_CHOICES = (
        ('Draft', 'Draft'),
        ('Published', 'Published'),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    featured_image = models.ImageField(upload_to='blog_images/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Draft')
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            original_slug = slugify(self.title)
            queryset = Post.objects.filter(slug__iexact=original_slug).count()
            count = 1
            slug = original_slug
            while(queryset):
                slug = f"{original_slug}-{count}"
                count += 1
                queryset = Post.objects.filter(slug__iexact=slug).count()
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at'] 

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user') 

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"