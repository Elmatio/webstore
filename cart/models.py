from django.db import models
from shop.models import Product


class Cart(models.Model):
    id_cart = models.PositiveIntegerField(default=1)
    products = models.ManyToManyField(Product,
                                      through='CartItem')
    session = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.id_cart}'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart,
                             related_name='cart',
                             on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='product',
                                on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'В корзине {self.quantity} товаров {self.product.name}.'
