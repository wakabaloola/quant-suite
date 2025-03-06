# core/views.py
from django.shortcuts import render
from django.db.models import Q
from blog.models import Post
from glossary.models import GlossaryTerm

def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')

def debug_view(request):
    return render(request, 'core/debug.html')

def site_search(request):
    query = request.GET.get('q', '')
    if query:
        # Search in blog posts
        blog_results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        ).distinct()

        # Search in glossary terms
        glossary_results = GlossaryTerm.objects.filter(
            Q(term__icontains=query) |
            Q(definition__icontains=query) |
            Q(category__icontains=query)
        ).distinct()
    else:
        blog_results = Post.objects.none()
        glossary_results = GlossaryTerm.objects.none()

    context = {
        'query': query,
        'blog_results': blog_results,
        'blog_count': blog_results.count(),
        'glossary_results': glossary_results,
        'glossary_count': glossary_results.count(),
        'total_count': blog_results.count() + glossary_results.count(),
    }
    return render(request, 'core/search_results.html', context)
