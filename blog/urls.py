# blog/urls.py
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('search/', views.search_posts, name='search_posts'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
]

