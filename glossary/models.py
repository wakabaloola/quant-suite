# glossary/models.py
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from markdownx.models import MarkdownxField
from django.utils.safestring import mark_safe
import markdown
import bleach
from bleach.sanitizer import ALLOWED_TAGS, ALLOWED_ATTRIBUTES

class GlossaryTerm(models.Model):
    """
    Defines financial terms with their definitions using MarkdownxField.

    Features:
        - Includes a slug field for nice URLs that's automatically generated from the term
        - Has a category field to organize terms by topic
        - Includes timestamps to track creation and updates
        - Has Meta options to order terms alphabetically and customize the display names in the admin
        - Overrides the save method to auto-generate a slug if one isn't provided
    """
    term = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    definition = MarkdownxField()
    category = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['term']
        verbose_name = 'Glossary Term'
        verbose_name_plural = 'Glossary Terms'

    def __str__(self):
        return self.term
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.term)
        super().save(*args, **kwargs)

    def formatted_definition(self):
        """
        Render the markdown content with LaTeX, code highlighting, and footnotes support.
        Returns:
            str: HTML-formatted definition with LaTeX and code syntax highlighting
        """
        # Define allowed HTML tags and attributes
        allowed_tags = list(ALLOWED_TAGS) + ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                                'img', 'pre', 'code', 'blockquote', 'em',
                                'strong', 'ul', 'ol', 'li', 'span', 'div',
                                'table', 'thead', 'tbody', 'tr', 'th', 'td',
                                'hr', 'br', 'a', 'sup', 'section', 'ol']
        allowed_attrs = ALLOWED_ATTRIBUTES.copy()
        allowed_attrs.update({
            'img': ['src', 'alt', 'title', 'class'],
            'a': ['href', 'title', 'class', 'target', 'rel', 'id'],
            'code': ['class'],
            'pre': ['class'],
            'span': ['class', 'style'],
            'div': ['class', 'style'],
            'section': ['class', 'id'],
            'ol': ['class', 'start'],
            'li': ['id'],
            'sup': ['id', 'class'],
            'h1': ['id'],
            'h2': ['id'],
            'h3': ['id'],
            'h4': ['id'],
            'h5': ['id'],
            'h6': ['id']  # Allow IDs on all heading levels
        })

        # Convert markdown to HTML with footnotes support
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',  # Includes tables, footnotes, etc.
            'markdown.extensions.codehilite',
            'markdown.extensions.sane_lists',
            'markdown.extensions.footnotes',  # Explicitly include footnotes
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code',
            'markdown.extensions.toc' # Add TOC extension for heading IDs
        ])
        html = md.convert(self.definition)

        # Sanitize HTML
        clean_html = bleach.clean(html, tags=allowed_tags, attributes=allowed_attrs)

        # Return marked safe HTML
        return mark_safe(clean_html)

    def get_absolute_url(self):
        """
        Returns the URL to access a particular glossary term instance on the website.

        This enables the "View on Site" button in the admin interface.
        """
        return reverse('glossary:glossary_detail', args=[self.slug])
