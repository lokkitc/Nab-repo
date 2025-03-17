from django.urls import path
from . import views
from django.contrib.auth.views import PasswordChangeDoneView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'auth'

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'), 
    path('logout/', views.logout_user, name='logout'), 
    path('register/', views.RegisterUser.as_view(), name='register'), 

    path('password-change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change-done/', PasswordChangeDoneView.as_view(template_name='auth/password_change_done.html'), name='password_change_done'), 

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
