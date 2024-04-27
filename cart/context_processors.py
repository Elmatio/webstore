from .cart import CartClass


def cart(request):
    cart = CartClass(request)
    end = ''
    if len(cart) > 1:
        if len(cart) < 5:
            end = 'а'
        else:
            end = 'ов'
    return {'cart': CartClass(request), 'end': end}
