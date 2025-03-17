from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.shortcuts import redirect
from product.models import Order
from .forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, CreateView
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
class LoginUser(LoginView):
    form_class =  LoginUserForm
    template_name = 'user/login.html'
    extra_context = {'title': 'Авторизация'}

    def get_success_url(self):
        return reverse_lazy('home')


def profile_user(request, pk):
    if request.user.is_authenticated:
        order = Order.objects.get(id=pk, user=request.user)
        orders = Order.objects.filter(user=request.user).order_by('-order_date')
        context = {
            'order': order,
            'orders': orders,
            }
        return render(request, 'user/profile.html', context)
    else:
        return redirect('user:login')


def cart(request, pk):
    order = Order.objects.get(id=pk, user=request.user)
    items = order.orderitem_set.all()
    context = {
            'order': order,
            'items': items,
            'count': items.count(),
            # 'bonus': bonus,
        }
    return render(request, 'user/cart.html', context)

def logout_user(request):
    logout(request)
    return redirect('home')

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'success': True,
                'message': 'Профиль успешно обновлен'
            })
        return JsonResponse({
            'success': False,
            'errors': form.errors
        })
    return JsonResponse({
        'success': False,
        'message': 'Метод не поддерживается'
    })


class RegisterUser(CreateView):
    model = get_user_model()
    form_class = RegisterUserForm
    template_name = 'user/register.html'
    success_url = reverse_lazy('user:login')
    

class ProfileUserView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'user/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(user=self.request.user).order_by('-order_date')
        return context

    def get_success_url(self):
        return reverse_lazy('user:profile', args=[self.object.pk])

class PasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('user:password_change_done') 
    template_name = 'user/password_change_form.html'
