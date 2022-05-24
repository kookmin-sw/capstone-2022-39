from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'title', 'category', 'work_time', 'call_number']
    list_display_links = ['title']
    list_filter = ['gather_count']
    search_fields = ['title']
    # form = PostForm