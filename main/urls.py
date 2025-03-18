from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('brands/', views.brands, name='brands'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

