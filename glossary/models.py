# glossary/models.py
from django.db import models
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
        Render the markdown content with LaTeX and code highlighting support.

        Returns:
            str: HTML-formatted definition with LaTeX and code syntax highlighting
        """
        # Define allowed HTML tags and attributes
        allowed_tags = list(ALLOWED_TAGS) + ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                                 'img', 'pre', 'code', 'blockquote', 'em',
                                 'strong', 'ul', 'ol', 'li', 'span', 'div',
                                 'table', 'thead', 'tbody', 'tr', 'th', 'td',
                                 'hr', 'br', 'a']
        allowed_attrs = ALLOWED_ATTRIBUTES.copy()
        allowed_attrs.update({
            'img': ['src', 'alt', 'title', 'class'],
            'a': ['href', 'title', 'class'],
            'code': ['class'],
            'pre': ['class'],
            'span': ['class', 'style'],
            'div': ['class', 'style']
        })

        # Convert markdown to HTML
        html = markdown.markdown(
            self.definition,
            extensions=['extra', 'codehilite', 'sane_lists', 'tables']
        )

        # Sanitize HTML
        clean_html = bleach.clean(html, tags=allowed_tags, attributes=allowed_attrs)

        # Return marked safe HTML
        return mark_safe(clean_html)
