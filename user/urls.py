from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'user'

urlpatterns = [
    path('login/', views.login_user, name='login'), # 127.0.0.1:8000/user/login/


    # path('<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
