# blog/models.py
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from django.utils.safestring import mark_safe
import markdown
import bleach
import re
from bleach.sanitizer import ALLOWED_TAGS, ALLOWED_ATTRIBUTES

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    content = MarkdownxField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Research Note'
        verbose_name_plural = 'Research Notes'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})
    
    def formatted_markdown(self):
        """
        Method to display formatted markdown content with rendered LaTeX, code highlighting, and footnotes
        """
        # Convert markdown to HTML with extensions including TOC
        md = markdown.Markdown(extensions=[
            'markdown.extensions.footnotes',
            'markdown.extensions.codehilite',
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code',
            'markdown.extensions.toc'  # Add TOC extension for heading IDs
        ])
        html = md.convert(self.content)
        
        # Add the rest of your existing code for sanitization
        # Important: Make sure 'id' is in the allowed attributes for headings
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
        
        # Look for <pre><code> without a class and add language-python
        html = re.sub(r'<pre><code>(?!\s*<)', '<pre><code class="language-python">', html)
        # Look for language specifiers in fenced code blocks and convert them to Prism format
        html = re.sub(r'<pre><code class="[^"]*language-([^"]+)">', r'<pre><code class="language-\1">', html)
        
        # Sanitize HTML
        clean_html = bleach.clean(html, tags=allowed_tags, attributes=allowed_attrs)
        
        # Return marked safe HTML
        return mark_safe(clean_html)
