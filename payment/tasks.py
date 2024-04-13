from io import BytesIO
from celery import shared_task
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from orders.models import Order


@shared_task
def payment_completed(order_id):
    """
    Задание для отправки PDF по почте.
    """
    order = Order.objects.get(id=order_id)
    # create invoice e-mail
    subject = f'СОМ - Заказ № {order.id}'
    message = 'Пожалуйста, найдите в приложении счет за вашу недавнюю покупку.'
    email = EmailMessage(subject,
                         message,
                         'admin@webstore.com',
                         [order.email])
    # generate PDF
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out,
                                          stylesheets=stylesheets)
    # attach PDF file
    email.attach(f'order_{order.id}.pdf',
                 out.getvalue(),
                 'application/pdf')
    # send e-mail
    email.send()
