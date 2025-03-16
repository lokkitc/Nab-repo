from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


from .forms import LoginUserForm

class LoginUser(LoginView):
    form_class =  LoginUserForm
    template_name = 'user/login.html'
    extra_context = {'title': 'Авторизация'}

    def get_success_url(self):
        return reverse_lazy('home')



def profile_user(request, pk):
    return render(request, 'user/profile.html')


def cart(request, pk):
    pass
