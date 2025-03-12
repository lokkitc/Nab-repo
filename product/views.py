from django.shortcuts import render

def product_detail(request, slug):
    data = {
        'title': 'Продукт',
    }
    return render(request, 'main/product.html', data)
