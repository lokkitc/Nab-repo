from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.shortcuts import redirect
from product.models import Order
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.views.generic import UpdateView
from .forms import ProfileUserForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


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

def payment(request):
    return render(request, 'main/payment.html')

def cart(request, pk):
    order = Order.objects.get(id=pk, user=request.user)
    items = order.orderitem_set.all()
    
    total_amount = order.total_amount
    user_balance = request.user.money 
    can_checkout = user_balance >= total_amount
    
    context = {
            'order': order,
            'items': items,
            'count': items.count(),
            'can_checkout': can_checkout,
            'user_balance': user_balance,
            # 'bonus': bonus,
        }
    return render(request, 'user/cart.html', context)



class ProfileUserView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'user/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(user=self.request.user).order_by('-order_date')
        return context

    def get_success_url(self):
        return reverse_lazy('auth:profile', args=[self.object.pk])



@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileUserForm(request.POST, request.FILES, instance=request.user)
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


def profile_view(request):
    if request.method == 'POST':
        form = ProfileUserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user:profile')
    else:
        form = ProfileUserForm(instance=request.user)
    
    return render(request, 'user/profile.html', {'form': form})


