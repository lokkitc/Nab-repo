from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import PasswordChangeDoneView

app_name = 'user'

urlpatterns = [


    path('profile/<int:pk>/', views.ProfileUserView.as_view(), name='profile'), # 127.0.0.1:8000/user/profile/34234/
    path('update-profile/', views.update_profile, name='update-profile'),
    path('cart/<int:pk>/', views.cart, name='cart'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
