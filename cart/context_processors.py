from .cart import Cart


def cart(request):
    cart = Cart(request)
    end = ''
    if len(cart) > 1:
        if len(cart) < 5:
            end = 'а'
        else:
            end = 'ов'
    return {'cart': Cart(request), 'end': end}
