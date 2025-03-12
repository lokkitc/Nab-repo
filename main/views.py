from django.shortcuts import render
from django.http import HttpResponse
from product.models import Product, Category, Review, Order, OrderItem

menu = [
    {'title': 'Главная', 'url_name': 'home'},
    {'title': 'Категории', 'url_name': 'category'},
    {'title': 'Регистрация', 'url_name': 'register'},
]



def home(request):
    data = {    
        'title': 'Главная страница',
    }
    return render(request, 'main/home.html', data)

def category(request, slug):
    data = {
        'title': 'Категория',
        'category': Category.objects.get(slug=slug),
        'products': Product.objects.filter(category__slug=slug)
    }
    return render(request, 'main/category.html', data)

def register(request):
    data = {
        'title': 'Регистрация',
    }
    return render(request, 'main/register.html', data)

