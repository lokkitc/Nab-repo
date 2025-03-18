from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'product'

urlpatterns = [ 
    path('', views.catalog, name='catalog'),
    path('product/<slug:slug>', views.product_detail, name='product_detail'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/', views.update_cart_item, name='update_cart_item'),
    path('cart/delete/', views.delete_cart_item, name='delete_cart_item'),
    path('add-review/<int:product_id>/', views.add_review, name='add_review'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

