# blog/admin.py
from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import Post

@admin.register(Post)
class PostAdmin(MarkdownxModelAdmin):    #admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'content')
    list_filter = ('created_at', 'updated_at')
