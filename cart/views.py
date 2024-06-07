from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from coupons.forms import CouponApplyForm
from shop.recommender import Recommender
from django.http import JsonResponse
from .models import CartItem, Cart
from .cart_funtions import *


def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)
    else:
        session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    quantity = int(request.POST.get('quantity', 1))
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart_item = get_object_or_404(CartItem, product__id=product_id)
    cart_item.delete()
    return redirect('cart:cart_detail')


def cart_detail(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.get(user=user)
    else:
        session_key = request.session.session_key
        cart = Cart.objects.get(session_key=session_key)
    cart_item = cart.cart.all()
    coupon_apply_form = CouponApplyForm()
    #Нахождение всех товаров в корзине
    cart_products = [item.product for item in cart_item]

    #Попытка извлечь айди купона
    coupon_id = request.session.get('coupon_id')
    coupon, discount = None, None
    if coupon_id:
        coupon = get_coupon(coupon_id)
        discount = get_discount(cart, coupon)

    total_price = get_total_price(cart)
    total_count = get_total_count(cart)
    subtotal_price = total_price
    if isinstance(discount, int):
        total_price -= discount
    r = Recommender()
    if cart_products:
        recommended_products = r.suggest_products_for(cart_products, max_results=4)
    else:
        recommended_products = []
    return render(request, 'cart/detail.html',
                  {'cart_item': cart_item,
                   'coupon_apply_form': coupon_apply_form,
                   'recommended_products': recommended_products,
                   'coupon': coupon,
                   'discount': discount,
                   'total_price': total_price,
                   'total_count': total_count,
                   'subtotal_price': subtotal_price})


@require_POST
def save_data_to_session(request):
    product_id = request.POST.get('product_id')
    product_count = request.POST.get('product_count')

    # Получить объекты товара и корзины
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        user = request.user
        cart, _ = Cart.objects.get_or_create(user=user)
    else:
        session_key = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_key=session_key)
    cart_item, _ = CartItem.objects.get_or_create(cart=cart, product=product)

    # Обновить количество товара в корзине
    cart_item.quantity = product_count
    cart_item.save()

    # Вернуть ответ JSON
    return JsonResponse({'message': 'Data received successfully'})
