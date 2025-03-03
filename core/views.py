# core/views.py
from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')

def debug_view(request):
    return render(request, 'core/debug.html')
