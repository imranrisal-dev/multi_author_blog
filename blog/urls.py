from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='home'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<slug:slug>/like/', views.like_toggle, name='like_toggle'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    
    # Author URLs
    path('dashboard/', views.author_dashboard, name='author_dashboard'),
    path('post/new', views.create_post, name='create_post'),
    path('post/<slug:slug>/edit/', views.edit_post, name='edit_post'),
    path('post/<slug:slug>/delete/', views.delete_post, name='delete_post'),
    
    # Author Profile
    path('author/<str:username>/', views.author_profile, name='author_profile'),
]