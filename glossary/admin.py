# glossary/admin.py
from django.contrib import admin
from .models import GlossaryTerm

@admin.register(GlossaryTerm)
class GlossaryTermAdmin(admin.ModelAdmin):
    """
    Admin configuration for GlossaryTerm model.
    
    Provides list display of terms with their categories and 
    creation dates, search functionality, and prepopulated slugs.
    """
    list_display = ('term', 'category', 'created_at')
    list_filter = ('category',)
    search_fields = ('term', 'definition')
    prepopulated_fields = {'slug': ('term',)}
    view_on_site = True
