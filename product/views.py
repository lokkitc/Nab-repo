from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Avg
from django.conf import settings
from decimal import Decimal
from .models import Product, Review, Category, Brand, Order, OrderItem
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import json

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
        
    selected_name = request.GET.get('name')
    print(f"Selected name: {selected_name}") 
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
    
    if selected_name:
        products = products.filter(name__icontains=selected_name)
    
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

    if not page_obj.object_list:
        no_products_message = "Нет доступных продуктов по вашему запросу."
    else:
        no_products_message = ""

    context = {
        'categories': categories,
        'brands': brands,
        'products': page_obj,
        'selected_category': selected_category,
        'selected_brands': selected_brands,
        'selected_name': selected_name,
        'price_min': price_min,
        'price_max': price_max,
        'sorting': sorting,
        'MEDIA_URL': settings.MEDIA_URL,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'no_products_message': no_products_message, 
    }
    
    return render(request, 'product/catalog.html', context)

@require_POST
@login_required
def add_to_cart(request):
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))
        
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Product not found'})
        
        if not product.is_in_stock():
            return JsonResponse({'success': False, 'error': 'Product out of stock'})
        
        if product.stock < quantity:
            return JsonResponse({
                'success': False, 
                'error': f'Недостаточно товара. Доступно: {product.stock}'
            })
        
        active_order = Order.get_active_order(request.user)
        
        if active_order:
            order = active_order
        else:
            order = Order.objects.create(
                user=request.user,
                status='pending',
                shipping_address=''
            )
        
        try:
            order_item = OrderItem.objects.get(order=order, product=product)
            if product.stock < (order_item.quantity + quantity):
                return JsonResponse({
                    'success': False,
                    'error': f'Недостаточно товара. В корзине: {order_item.quantity}, на складе: {product.stock}'
                })
            order_item.quantity += quantity
            order_item.save()
        except OrderItem.DoesNotExist:
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity
            )
        
        return JsonResponse({
            'success': True,
            'cart_id': order.id,
            'total_items': order.orderitem_set.count(),
            'remaining_stock': product.stock
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'})
    except ValueError as e:
        return JsonResponse({'success': False, 'error': str(e)})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@require_POST
@login_required
def update_cart_item(request):
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        quantity = int(data.get('quantity', 1))
        
        order_item = get_object_or_404(OrderItem, id=item_id, order__user=request.user)
        product = order_item.product
        
        if product.stock + order_item.quantity < quantity:
            return JsonResponse({
                'success': False,
                'error': f'Недостаточно товара. Доступно: {product.stock + order_item.quantity}'
            })
        
        product.stock += order_item.quantity
        product.save()
        
        order_item.quantity = quantity
        order_item.save()
        
        return JsonResponse({
            'success': True,
            'quantity': order_item.quantity,
            'total': float(order_item.total),
            'cart_total': float(order_item.order.total_amount)
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@require_POST
@login_required
def delete_cart_item(request):
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        
        order_item = get_object_or_404(OrderItem, id=item_id, order__user=request.user)
        
        product = order_item.product
        product.stock += order_item.quantity
        product.save()
        
        order = order_item.order
        
        order_item.delete()
        
        order.total_amount = order.get_total()
        order.save()
        
        return JsonResponse({
            'success': True,
            'cart_total': float(order.total_amount),
            'items_count': order.orderitem_set.count()
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
