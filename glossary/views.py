# glossary/views.py
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import GlossaryTerm

class GlossaryListView(ListView):
    """
    View for displaying a list of all glossary terms.

    Includes functionality for filtering by first letter
    and category, sorted alphabetically.
    """
    model = GlossaryTerm
    context_object_name = 'terms'
    template_name = 'glossary/glossary_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add all unique first letters of terms for alphabet filtering
        context['letters'] = sorted(set(term.term[0].upper() for term in GlossaryTerm.objects.all()))
        # Add all unique categories for category filtering
        context['categories'] = GlossaryTerm.objects.values_list('category', flat=True).distinct().order_by('category')
        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by first letter if specified
        letter = self.request.GET.get('letter')
        if letter:
            queryset = queryset.filter(term__istartswith=letter)

        # Filter by category if specified
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)

        return queryset

class GlossaryDetailView(DetailView):
    """
    View for displaying the details of a single glossary term.

    Retrieves the term based on its slug and displays its
    full definition with markdown rendering.
    """
    model = GlossaryTerm
    context_object_name = 'term'
    template_name = 'glossary/glossary_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get related terms (same category, excluding current term)
        current_term = self.get_object()
        if current_term.category:
            related_terms = GlossaryTerm.objects.filter(
                    category=current_term.category
            ).exclude(
                    id=current_term.id
            )[:5]   # limit to 5 terms
            context['related_terms'] = related_terms  # Fixed key name

        # Add highlight term if it exists in URL
        highlight = self.request.GET.get('highlight', '')
        if highlight:
            context['highlight_term'] = highlight

        return context

def search_glossary(request):
    """
    View for searching glossary terms.

    Searches through term names, definitions, and categories
    based on the query parameter.
    """
    query = request.GET.get('q', '')
    if query:
        results = GlossaryTerm.objects.filter(
            Q(term__icontains=query) |
            Q(definition__icontains=query) |
            Q(category__icontains=query)
        ).distinct()
    else:
        results = GlossaryTerm.objects.none()

    context = {
        'query': query,
        'results': results,
        'count': results.count(),
    }
    return render(request, 'glossary/search_results.html', context)
