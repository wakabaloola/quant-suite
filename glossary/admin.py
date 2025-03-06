# glossary/admin.py
from django import forms
from django.contrib import admin
from markdownx.widgets import MarkdownxWidget
from .models import GlossaryTerm

class GlossaryTermAdminForm(forms.ModelForm):
    """
    Custom form for the GlossaryTerm admin with improved MarkdownX editor
    """
    class Meta:
        model = GlossaryTerm
        fields = '__all__'
        widgets = {
            'definition': MarkdownxWidget(attrs={
                'class': 'markdownx-editor',
                'data-markdownx-editor-resizable': 'false',  # Helps prevent auto-grow issue
                'style': 'min-height: 400px;' # Remove fixed width here
            }),
        }

@admin.register(GlossaryTerm)
class GlossaryTermAdmin(admin.ModelAdmin):
    """
    Admin configuration for GlossaryTerm model.
    
    Provides list display of terms with their categories and 
    creation dates, search functionality, and prepopulated slugs.
    Uses a custom form with an improved MarkdownX editor.
    """
    form = GlossaryTermAdminForm
    list_display = ('term', 'category', 'created_at')
    list_filter = ('category',)
    search_fields = ('term', 'definition')
    prepopulated_fields = {'slug': ('term',)}
    view_on_site = True
    
    fieldsets = (
        (None, {
            'fields': ('term', 'slug', 'category'),
        }),
        ('Definition', {
            'fields': ('definition',),
            'classes': ('wide', 'extrapretty'),
        }),
    )

    class Media:
        css = {
            'all': ('css/admin-custom.css',)
        }
