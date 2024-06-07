from django import template

register = template.Library()


@register.filter
def discounted_price(price, discount):
    return price - (price * discount // 100)
