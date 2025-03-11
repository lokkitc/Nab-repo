from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), # 127.0.0.1:8000/
    path('product/<slug:slug>', views.product, name='product'), # 127.0.0.1:8000/product/iphone-15-pro-max
    path('category/<slug:slug>', views.category, name='category'), # 127.0.0.1:8000/category/iphone
]

