from product.models import Product, Category, Review, Order, OrderItem, Brand

def global_context(request):
    count = 0
    order_count = 0
    if request.user.is_authenticated:
        try:
            order = Order.objects.filter(user=request.user).first()
            order_count = Order.objects.filter(user=request.user).count()
            if order:
                count = order.orderitem_set.count()
                
        except Order.DoesNotExist:
            pass

    context = {
        'order_count': order_count,
        'count': count,
    }
    return context

