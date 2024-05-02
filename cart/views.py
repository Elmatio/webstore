from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import CartClass
from .forms import AddProductForm
from coupons.forms import CouponApplyForm
from shop.recommender import Recommender
from django.http import JsonResponse
from django.core.serializers import serialize
from .models import CartItem, Cart
from django.contrib.sessions.models import Session


# @require_POST
# def cart_add(request, product_id):
#     cart = CartClass(request)
#     product = get_object_or_404(Product, id=product_id)
#     form = AddProductForm(request.POST)
#     if form.is_valid():
#         cd = form.cleaned_data
#         cart.add(product=product,
#                  quantity=cd['quantity'],
#                  override_quantity=cd['override'])
#     return redirect('cart:cart_detail')

def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    session_key = request.session.session_key
    cart, created = Cart.objects.get_or_create(session_key=session_key)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    quantity = int(request.POST.get('quantity', 1))
    if not created:
        cart_item.quantity += quantity
    cart_item.save()
    return redirect('cart:cart_detail')

# @require_POST
# def cart_remove(request, product_id):
#     cart = CartClass(request)
#     product = get_object_or_404(Product, id=product_id)
#     cart.remove(product)
#     return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart_item = get_object_or_404(CartItem, product__id=product_id)
    cart_item.delete()
    return redirect('cart:cart_detail')


def cart_detail(request):
    session_key = request.session.session_key
    #Finding the cart by ID session
    cart = Cart.objects.get(session_key=session_key)
    cart_item = cart.cart.all()
    #Assigning a form to a variable
    coupon_apply_form = CouponApplyForm()
    #Finding all products in current cart
    cart_products = [item.product for item in cart_item]
    cart_item_copy = CartItem()

    #Trying to extract coupon ID
    coupon_id = request.session.get('coupon_id')
    coupon, discount = None, None
    if coupon_id:
        coupon = cart_item_copy.coupon(coupon_id)
        discount = cart_item_copy.get_discount(coupon)
    total_price = cart_item_copy.get_total_price() - discount

    r = Recommender()
    if cart_products:
        recommended_products = r.suggest_products_for(cart_products, max_results=4)
    else:
        recommended_products = []
    return render(request, 'cart/detail.html',
                  {'cart_item': cart_item,
                   'coupon_apply_form': coupon_apply_form,
                   'recommended_products': recommended_products,
                   'cart_item_copy': cart_item_copy,
                   'coupon': coupon,
                   'discount': discount,
                   'total_price': total_price})



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
#
#     # Load saved data from session if available
#     saved_product_count = request.session.get('product_count')
#     if saved_product_count is not None:
#         # Update cart with saved product count
#         cart.update_product_count(saved_product_count)
#
#     return render(request,
#                   'cart/detail.html',
#                   {'cart': cart,
#                    'coupon_apply_form': coupon_apply_form,
#                    'recommended_products': recommended_products})


@require_POST
def save_data_to_session(request):
    product_id = request.POST.get('product_id')
    product_count = request.POST.get('product_count')

    # Получить объекты товара и корзины
    product = get_object_or_404(Product, id=product_id)
    session_key = request.session.session_key
    cart, _ = Cart.objects.get_or_create(session_key=session_key)
    cart_item, _ = CartItem.objects.get_or_create(cart=cart, product=product)

    # Обновить количество товара в корзине
    cart_item.quantity = product_count
    cart_item.save()

    # Вернуть ответ JSON
    return JsonResponse({'message': 'Data received successfully'})
