from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), # 127.0.0.1:8000/
    path('category/<slug:slug>', views.category, name='category'), # 127.0.0.1:8000/category/iphone
    
    path('register/', views.register, name='register')
]

