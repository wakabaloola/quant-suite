# glossary/urls.py
from django.urls import path
from . import views

app_name = 'glossary'

urlpatterns = [
    path('', views.GlossaryListView.as_view(), name='glossary_list'),
    path('search/', views.search_glossary, name='search_glossary'),
    path('<slug:slug>/', views.GlossaryDetailView.as_view(), name='glossary_detail'),
]
