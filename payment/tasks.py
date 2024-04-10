from io import BytesIO
from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order
import weasyprint


@shared_task
def payment_completed(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully paid.
    """
    order = Order.objects.get(id=order_id)
    subject = f'СОМ - Счёт-фактура №  {order.id}'
    message = 'Пожалуйста, приложите к письму счёт вашей недавней покупки'
    email = EmailMessage(subject,
                         message,
                         'admin@webstore.com',
                         [order.email])
    html = render_to_string('orders/order/pdf.html',
                            {'order': order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out,
                                           stylesheets=stylesheets)
    email.attach(f'order_{order.id}.pdf',
                 out.getvalue(),
                 'application/pdf')
    email.send()
