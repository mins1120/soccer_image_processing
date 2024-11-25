from django.db.models import Count
from django.shortcuts import render

def index(request):
    return render(request, 'home.html')