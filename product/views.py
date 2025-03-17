from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Avg
from django.conf import settings
from decimal import Decimal
from .models import Product, Review, Category, Brand

BONUS_RATE = Decimal('0.05')
CREDIT_MONTHS = Decimal('60')
INSTALLMENT_MONTHS = Decimal('24')
PRODUCTS_PER_PAGE = 12

def product_detail(request, slug):

    try:
        product = get_object_or_404(
            Product.objects.annotate(avg_rating=Avg('reviews__rating')),
            slug=slug
        )
        
        price = product.price if isinstance(product.price, Decimal) else Decimal(str(product.price))
        
        context = {
            'product': product,
            'bonus': int(price * BONUS_RATE),
            'credit_monthly': int(price / CREDIT_MONTHS),
            'installment_monthly': int(price / INSTALLMENT_MONTHS),
        }
        return render(request, 'product/product.html', context)
    except Product.DoesNotExist:
        return render(request, 'product/not_found.html', status=404)

def catalog(request):

    categories = Category.objects.all()
    selected_category = str(request.GET.get('category')) if request.GET.get('category') else ''
    if selected_category:
        brands = Brand.objects.filter(
            category__id=selected_category
        ).distinct()
    else:
        brands = Brand.objects.all()
        
    selected_brands = request.GET.getlist('brand')
    price_min = request.GET.get('priceMin')
    price_max = request.GET.get('priceMax')
    sorting = request.GET.get('sorting')
    page_number = request.GET.get('page', 1)

    products = Product.objects.all().annotate(
        avg_rating=Avg('reviews__rating')
    ).reverse()

    if selected_category:
        products = products.filter(category__id=selected_category)
    
    if selected_brands:
        products = products.filter(brand__id__in=selected_brands)
    
    try:
        if price_min:
            price_min = Decimal(price_min)
            products = products.filter(price__gte=price_min)
        if price_max:
            price_max = Decimal(price_max)
            products = products.filter(price__lte=price_max)
    except (ValueError, TypeError):
        price_min = None
        price_max = None


    sort_mapping = {
        'price_asc': 'price',
        'price_desc': '-price',
        'name': 'name',
        'score': '-avg_rating',
        'newest': '-created_at'
    }
    
    sort_field = sort_mapping.get(sorting)
    if sort_field:
        products = products.order_by(sort_field)
    else:
        products = products.order_by('-created_at')

    paginator = Paginator(products, PRODUCTS_PER_PAGE)
    try:
        page_obj = paginator.page(page_number)
    except:
        page_obj = paginator.page(1)

    context = {
        'categories': categories,
        'brands': brands,
        'products': page_obj,
        'selected_category': selected_category,
        'selected_brands': selected_brands,
        'price_min': price_min,
        'price_max': price_max,
        'sorting': sorting,
        'MEDIA_URL': settings.MEDIA_URL,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    }
    
    return render(request, 'product/catalog.html', context)
