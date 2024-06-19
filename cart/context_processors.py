from .models import Cart, Cart_items

def cart_count(request):
    cart_count = 0
    cart_id = _cart_id(request)
    if cart_id:
        try:
            cart = Cart.objects.get(cart_id=cart_id)
            cart_count = Cart_items.objects.filter(cart=cart).count()
        except Cart.DoesNotExist:
            pass
    return {'cart_count': cart_count}

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart
