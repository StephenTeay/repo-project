# search/views.py
from django.db.models import Q
from django.views.generic import ListView
from projects.models import Project
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

class AdvancedSearchView(SearchView):
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')
        
        if search_query:
            vector = SearchVector('title', weight='A') + \
                    SearchVector('abstract', weight='B') + \
                    SearchVector('keywords', weight='C')
            query = SearchQuery(search_query)
            queryset = queryset.annotate(
                search=vector,
                rank=SearchRank(vector, query)
            ).filter(search=query).order_by('-rank')
            
        return queryset

class SearchView(ListView):
    model = Project
    template_name = 'search/results.html'
    paginate_by = 10
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        department = self.request.GET.get('department')
        year = self.request.GET.get('year')
        author = self.request.GET.get('author')
        
        queryset = super().get_queryset().filter(is_approved=True)
        
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(abstract__icontains=query) |
                Q(keywords__icontains=query)
            )
        
        if department:
            queryset = queryset.filter(department__id=department)
            
        if year:
            queryset = queryset.filter(year=year)
            
        if author:
            queryset = queryset.filter(authors__username__icontains=author)
            
        return queryset.distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context
