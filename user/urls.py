from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView as LogoutUser
app_name = 'user'

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'), # 127.0.0.1:8000/user/login/
    path('logout/', LogoutUser.as_view(next_page='user:login', http_method_names=['get', 'post']), name='logout'), # 127.0.0.1:8000/user/logout/

    path('profile/<int:pk>/', views.profile_user, name='profile'), # 127.0.0.1:8000/user/profile/34234/
    path('cart/<int:pk>/', views.cart, name='cart'), # 127.0.0.1:8000/user/cart/34234/

    # path('<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
