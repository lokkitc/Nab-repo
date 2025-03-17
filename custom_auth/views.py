from django.shortcuts import render 
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from product.models import Order, Product, Brand, Review, Category, OrderItem
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth import get_user_model
from .forms import LoginUserForm, RegisterUserForm, UserPasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import logout
from django.shortcuts import redirect


# Create your views here.
class LoginUser(LoginView):
    form_class =  LoginUserForm
    template_name = 'auth/login.html'
    extra_context = {'title': 'Авторизация'}

    def get_success_url(self):
        return reverse_lazy('home')


class RegisterUser(CreateView):
    model = get_user_model()
    form_class = RegisterUserForm
    template_name = 'auth/register.html'
    success_url = reverse_lazy('auth:login')
    


class PasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('auth:password_change_done') 
    template_name = 'auth/password_change_form.html'

def logout_user(request):
    logout(request)
    return redirect('home')