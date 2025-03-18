from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), # 127.0.0.1:8000/
    path('about/', views.about, name='about'), # 127.0.0.1:8000/about/
    path('brands/', views.brands, name='brands'), # 127.0.0.1:8000/brands/
    # path('register/', views.register, name='register')
]

