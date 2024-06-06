from .models import CartItem, Cart
from coupons.models import Coupon


def total_price(item):
    return item.product.price * item.quantity


def get_total_price(cart):
    items = cart.cart.all()
    return sum(total_price(item) for item in items)


def get_total_count(cart):
    items = cart.cart.all()
    return sum([item.quantity for item in items])


def get_coupon(coupon_id=None):
    if coupon_id:
        try:
            return Coupon.objects.get(id=coupon_id)
        except Coupon.DoesNotExist:
            pass
    return None


def get_discount(cart, coupon=None):
    if coupon:
        return int((coupon.discount / 100) \
                   * get_total_price(cart))
    return 0


def get_total_price_after_discount(cart):
    items = cart.cart.all()
    return get_total_price(cart) - get_discount(cart)
