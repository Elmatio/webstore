from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint
from .models import OrderItem, Order
from .forms import OrderCreateForms
from .tasks import order_created
from cart.models import Cart, CartItem


def order_create(request):
    session_key = request.session.session_key
    # Finding the cart by ID session
    cart = Cart.objects.get(session_key=session_key)
    cart_item = cart.cart.all()
    cart_item_copy = CartItem()
    discount = None
    coupon = cart_item_copy.coupon(request.session.get('coupon_id'))
    total_price = cart_item_copy.get_total_price()
    if request.method == 'POST':
        form = OrderCreateForms(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if coupon:
                discount = cart_item_copy.get_discount(coupon)
                order.coupon = coupon
                order.discount = discount
                total_price -= discount
            order.save()
            for item in cart_item:
                OrderItem.objects.create(order=order,
                                        product=item.product,
                                        price=item.product.price,
                                        quantity=item.quantity)
            # clear the cart
            CartItem.objects.all().delete()
            # launch asynchronous task
            order_created.delay(order.id)
            # set the order in the session
            request.session['order_id'] = order.id
            # redirect for payment
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForms()
    return render(request,
                  'orders/order/create.html',
                  {'cart_item': cart_item, 'form': form,
                   'coupon': coupon, 'discount': discount,
                   'total_price': total_price})


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order': order})


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html',
                            {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response,
        stylesheets=[weasyprint.CSS(
            settings.STATIC_ROOT / 'css/pdf.css')])
    return response