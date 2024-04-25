from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import AddProductForm
from coupons.forms import CouponApplyForm
from shop.recommender import Recommender
from django.http import JsonResponse



# Create your views here.
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = AddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


# def cart_detail(request):
#     cart = Cart(request)
#     for item in cart:
#         item['update_quantity_form'] = AddProductForm(initial={
#             'quantity': item['quantity'],
#             'override': True})
#     coupon_apply_form = CouponApplyForm()
#     r = Recommender()
#     cart_products = [item['product'] for item in cart]
#     if cart_products:
#         recommended_products = r.suggest_products_for(cart_products,
#                                                       max_results=4)
#     else:
#         recommended_products = []
#     return render(request,
#                   'cart/detail.html',
#                   {'cart': cart,
#                    'coupon_apply_form': coupon_apply_form,
#                    'recommended_products': recommended_products})


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = AddProductForm(initial={
            'quantity': item['quantity'],
            'override': True})
    coupon_apply_form = CouponApplyForm()
    r = Recommender()
    cart_products = [item['product'] for item in cart]
    if cart_products:
        recommended_products = r.suggest_products_for(cart_products,
                                                      max_results=4)
    else:
        recommended_products = []

    # Load saved data from session if available
    saved_product_count = request.session.get('product_count')
    if saved_product_count is not None:
        # Update cart with saved product count
        cart.update_product_count(saved_product_count)

    return render(request,
                  'cart/detail.html',
                  {'cart': cart,
                   'coupon_apply_form': coupon_apply_form,
                   'recommended_products': recommended_products})


def save_data_to_session(request):
    if request.method == 'POST':
        # Получаем данные из запроса
        received_data = request.POST.get('product_count')  # Получаем значение по ключу 'key'

        # Сохраняем данные в сессии
        request.session['product_count'] = received_data  # Замените 'your_key' на свой ключ

        # Возвращаем JSON ответ клиенту
        return JsonResponse({'message': 'Data saved successfully'})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=400)
