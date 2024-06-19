from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Wishlist
from store.models import product
from django.contrib import messages
from cart.models import Cart_items, Cart
from cart.views import add_cart

# Create your views here.
def wishlist(request):
    user = request.user
    Product = Wishlist.objects.filter(user=user)
    context = {
        'product': Product
    }
    return render(request, 'store/wishlist.html', context)


@login_required
def add_to_wishlist(request, product_id):
    Product = get_object_or_404(product, id=product_id)
    user = request.user
    wishlist_item, created = Wishlist.objects.get_or_create(user=user, product=Product)
    if created:
        messages.success(request, "Added to wishlist")
    else:
        messages.error(request, "Item already added to wishlist")
    return redirect('wishlist',)


@login_required
def wishlist_to_cart(request, p_id):
    
    add_cart(request, p_id)
    try:
        wishlist_item = Wishlist.objects.get(user=request.user, product_id=p_id)
        wishlist_item.delete()
        messages.success(request, "Product moved from wishlist to cart")
    except Wishlist.DoesNotExist:
        messages.warning(request, "Product not found in wishlist")
    
    return redirect('wishlist')