from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('<slug:slug>', views.product_detail, name='product_detail'), # 127.0.0.1:8000/product/iphone-15-pro-max
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

