from celery import shared_task
from django.core.mail import send_mail
from .models import Order


@shared_task
def order_created(order_id):
    """
    Задание поОтправке сообщений
    по электронной почте
    """
    order = Order.objects.get(id=order_id)
    subject = f'Заказ номер {order.id}'
    message = f'Уважаемый {order.first_name}, \n\n' \
              f'Вы успешно оформили заказ.' \
              f'Номер вашего заказа - {order.id}.'
    mail_sent = send_mail(subject,
                          message,
                          'admin@webstore.com',
                          [order.email])
    return mail_sent
