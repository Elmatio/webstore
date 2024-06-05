from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.views.generic import CreateView

from shop.models import Product
from .forms import LoginForm, RegistrationForm, UserEditForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from orders.models import Order, OrderItem
from .models import CustomUser


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


@login_required
def profile(request, user_id):
    orders = Order.objects.filter(user=request.user)
    order_items = [OrderItem.objects.filter(order=order) for order in orders]
    products = [item.product for orders in order_items for item in orders]
    user = user_id
    profile = CustomUser.objects.get(id=user)
    return render(request,
                  'account/profile.html',
                  {'profile': profile, 'products': products})


@login_required
def edit(request):
    profile = get_object_or_404(CustomUser, id=request.user.id)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account:profile', user_id=request.user.id)
    else:
        form = UserEditForm(instance=profile)
    return render(request,
                  'account/edit.html',
                  {'form': form})
