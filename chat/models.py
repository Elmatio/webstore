from django.db import models
from account.models import CustomUser


class Message(models.Model):
    user = models.ForeignKey(CustomUser,
                             verbose_name='chat_user',
                             on_delete=models.CASCADE)
    user_to = models.ForeignKey(CustomUser,
                                related_name='chat_admin',
                                on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
