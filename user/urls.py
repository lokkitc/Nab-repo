from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import PasswordChangeDoneView

app_name = 'user'

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'), # 127.0.0.1:8000/user/login/
    path('logout/', views.logout_user, name='logout'), # 127.0.0.1:8000/user/logout/
    path('register/', views.RegisterUser.as_view(), name='register'), # 127.0.0.1:8000/user/register/

    path('password-change/', views.PasswordChangeView.as_view(), name='password_change'), # 127.0.0.1:8000/user/password-change/
    path('password-change-done/', PasswordChangeDoneView.as_view(template_name='user/password_change_done.html'), name='password_change_done'), # 127.0.0.1:8000/user/password-change-done/

    path('profile/<int:pk>/', views.ProfileUserView.as_view(), name='profile'), # 127.0.0.1:8000/user/profile/34234/
    path('update-profile/', views.update_profile, name='update-profile'),
    path('cart/<int:pk>/', views.cart, name='cart'), # 127.0.0.1:8000/user/cart/34234/
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
