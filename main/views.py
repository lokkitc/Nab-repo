from django.shortcuts import render
from product.models import Product, Brand
from django.db.models import Avg
from django.contrib.auth.decorators import login_required

menu = [
    {'title': 'Главная', 'url_name': 'home'},
    {'title': 'Категории', 'url_name': 'category'},
    {'title': 'Регистрация', 'url_name': 'register'},
]

def about(request):
    return render(request, 'main/about.html')

def home(request):

    data = {    

        'title': 'Главная страница',
        'brands': Brand.objects.all(),
        'products': Product.objects.all().annotate(avg_rating=Avg('reviews__rating')),
        'most_popular_product': Product.objects.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating').first(),
        'most_expensive_product': Product.objects.order_by('-price').first(),
        'user': request.user,

    }
    return render(request, 'main/home.html', data)


def register(request):
    data = {
        'title': 'Регистрация',
    }
    return render(request, 'main/register.html', data)


def brands(request):
    data = {
        'title': 'Бренды',
        'brands': Brand.objects.all(),
    }
    return render(request, 'main/brands.html', data)

