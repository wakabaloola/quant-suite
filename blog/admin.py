# blog/admin.py
from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import Post

@admin.register(Post)
class PostAdmin(MarkdownxModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'content')
    list_filter = ('created_at', 'updated_at')
    
    # Custom admin header
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = 'Research Notes'
        return super().changelist_view(request, extra_context=extra_context)
    
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = 'Research Notes'
        return super().changeform_view(request, object_id, form_url, extra_context)
