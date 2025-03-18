from product.models import Product, Category, Review, Order, OrderItem, Brand
from decimal import InvalidOperation, Decimal

def global_context(request):
    count = 0
    order_count = 0
    if request.user.is_authenticated:
        try:
            order = Order.objects.filter(user=request.user).first()
            order_count = Order.objects.filter(user=request.user).count()
            if order:
                count = order.orderitem_set.count()
                
        except (Order.DoesNotExist, InvalidOperation):
            pass

    context = {
        'order_count': order_count,
        'count': count,
    }
    return context

