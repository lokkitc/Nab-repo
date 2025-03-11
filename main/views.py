from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'main/home.html')

def product(request, slug):
    return render(request, 'main/product.html', {'slug': slug})
