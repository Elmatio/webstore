from django.shortcuts import render, redirect
from .models import OrderItem
from .forms import OrderCreateForms
from cart.cart import Cart
from .tasks import order_created
from django.urls import reverse


# Create your views here.
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForms(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            #Запуск асинхронного задания
            order_created.delay(order.id)
            request.session['order_id'] = order.id
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForms()
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})
