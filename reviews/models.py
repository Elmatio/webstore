from django.db import models

from account.models import CustomUser
from shop.models import Product


# Create your models here.
class Review(models.Model):
    user = models.ForeignKey(CustomUser,
                             verbose_name='user',
                             on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                verbose_name='product',
                                on_delete=models.CASCADE)
    text = models.TextField('Комментарий', max_length=5000)

    def __str__(self):
        return f'{self.user.first_name} - {self.product}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
