from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.views.generic import CreateView

from .forms import LoginForm, RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from .models import Profile


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('shop:product_list')
                else:
                    return HttpResponse('Заблокированный аккаунт')
            else:
                return HttpResponse('Ошибка авторизации')
    else:
        form = LoginForm()
    return render(request,
                  'account/login.html',
                  {'form': form})


def user_logout(request):
    logout(request)
    return redirect('shop:product_list')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()
            #Profile.objects.create(user=username)
            return redirect('shop:product_list')
    else:
        form = RegistrationForm()
    return render(request,
                  'account/registration.html',
                  {'form': form})