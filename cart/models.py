from django.db import models
from shop.models import Product
from django.conf import settings
from coupons.models import Coupon
from decimal import Decimal


class Cart(models.Model):
    id_cart = models.PositiveIntegerField(default=1)
    products = models.ManyToManyField(Product,
                                      through='CartItem')
    session = models.CharField(max_length=255, null=True, blank=True)
    session_key = models.CharField(max_length=100, unique=True)
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
    session = models.CharField(max_length=255, null=True, blank=True)

    def total_price(self):
        return self.product.price * self.quantity

    def get_total_price(self):
        items = CartItem.objects.all()
        return sum(item.total_price() for item in items)

    def get_total_count(self):
        items = CartItem.objects.all()
        return sum([item.quantity for item in items])

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def coupon(self, coupon_id=None):
        if coupon_id:
            try:
                return Coupon.objects.get(id=coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    def get_discount(self, coupon=None):
        if coupon:
            return int((coupon.discount / 100) \
                        * self.get_total_price())
        return 0

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'В корзине {self.quantity} товаров {self.product.name}.'
