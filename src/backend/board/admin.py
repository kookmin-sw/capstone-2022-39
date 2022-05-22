from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass
    # list_display = [""]
    # list_display_links = [""]
