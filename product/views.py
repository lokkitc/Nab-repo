from django.shortcuts import render, get_object_or_404
from .models import Product
from decimal import Decimal

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    price = product.price if isinstance(product.price, Decimal) else Decimal(str(product.price))
    
    context = {
        'product': product,
        'bonus': int(price * Decimal('0.05')),
        'credit_monthly': int(price / Decimal('60')),
        'installment_monthly': int(price / Decimal('24')),
    }
    return render(request, 'product/product.html', context)