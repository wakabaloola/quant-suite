# blog/models.py
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    content = MarkdownxField()   #models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
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
        Method to display formatted markdown content with rendered LaTeX and code highlighting
        """
        # Get the standard Markdown conversion
        html = markdownify(self.content)

        # Ensure code blocks have the proper class for Prism
        import re
        # Look for <pre><code> without a class and add language-python
        html = re.sub(r'<pre><code>(?!\s*<)', '<pre><code class="language-python">', html)
        # Look for language specifiers in fenced code blocks and convert them to Prism format
        html = re.sub(r'<pre><code class="[^"]*language-([^"]+)">', r'<pre><code class="language-\1">', html)

        return html
