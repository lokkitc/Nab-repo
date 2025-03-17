from product.models import Product, Category, Review, Order, OrderItem, Brand

def global_context(request):
    count = 0
    if request.user.is_authenticated:
        try:
            order = Order.objects.filter(user=request.user).first()
            if order:
                count = order.orderitem_set.count()
        except Order.DoesNotExist:
            pass

    context = {
        'count': count,
    }
    return context

