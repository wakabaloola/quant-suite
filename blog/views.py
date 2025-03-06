# blog/views.py
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Post

class PostListView(ListView):
    model = Post
    template_name = 'research/post_list.html'  # Note: is this a typo? Should it be 'blog/post_list.html'?
    context_object_name = 'posts'
    paginate_by = 10

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        
        # Get the formatted markdown content
        formatted_content = self.object.formatted_markdown()
        
        # Check if there's a highlight parameter
        highlight = self.request.GET.get('highlight', '')
        if highlight:
            # Pass the highlight term to the template
            context['highlight_term'] = highlight
        
        # Add formatted_content to the context
        context['formatted_content'] = formatted_content
        return context

def search_posts(request):
    query = request.GET.get('q', '')
    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        ).distinct()
    else:
        results = Post.objects.none()

    context = {
        'query': query,
        'results': results,
        'count': results.count(),
    }
    return render(request, 'blog/search_results.html', context)
