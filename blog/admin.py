from django.contrib import admin
from .models import Category, Tag, Post, Comment, Like

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'view_count', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Like)