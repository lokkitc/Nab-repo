from django.shortcuts import render
from django.http import HttpResponse
from product.models import Product, Category, Review, Order, OrderItem
from django.db.models import Q, Avg
from django.shortcuts import redirect

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


def category(request):
    categories = Category.objects.all()
    
    selected_category = request.GET.get('category')
    price_min = request.GET.get('priceMin')
    price_max = request.GET.get('priceMax')
    sorting = request.GET.get('sorting')
    
    products = Product.objects.all().annotate(avg_rating=Avg('reviews__rating')).reverse()
    
    if selected_category:
        products = products.filter(category__slug=selected_category)
    
    if price_min and price_min.isdigit():
        products = products.filter(price__gte=price_min)
    if price_max and price_max.isdigit():
        products = products.filter(price__lte=price_max)
    
    if sorting:
        sort_mapping = {
            'price_asc': 'price',
            'price_desc': '-price',
            'name': 'name',
            'score': 'avg_rating',
            'newest': '-created_at'
        }
        sort_field = sort_mapping.get(sorting)
        if sort_field:
            products = products.order_by(sort_field)
    
    context = {
        'categories': categories,
        'products': products,
        'selected_category': selected_category,
        'price_min': price_min,
        'price_max': price_max,
        'sorting': sorting
    }
    
    return render(request, 'main/category.html', context)


def register(request):
    data = {
        'title': 'Регистрация',
    }
    return render(request, 'main/register.html', data)

