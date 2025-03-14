from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

from .forms import LoginForm

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user and user.is_active:
                login(request, user)
                return redirect('home')
            else:
                form.add_error('password', 'Неверный логин или пароль')
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form})    

def logout_user(request):
    logout(request)
    return redirect('home')
