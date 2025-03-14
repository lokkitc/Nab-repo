from django.shortcuts import render
from django.http import HttpResponse
from product.models import Product, Category, Review, Order, OrderItem
from django.db.models import Q, Avg
from django.shortcuts import redirect
from django.conf import settings

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


def register(request):
    data = {
        'title': 'Регистрация',
    }
    return render(request, 'main/register.html', data)

