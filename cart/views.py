from django.shortcuts import render, redirect
from .models import Cart, Cart_items, Address
from store.models import product
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from coupon.models import Coupon


# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product_instance = product.objects.get(id=product_id)
    
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        
    cart.save()
    
    try:
        cart_item = Cart_items.objects.get(cart=cart, product=product_instance)
        if cart_item.quantity > 5:
            messages.error(request, 'Maximum quantity per user has been reached')               
        elif cart_item.quantity < product_instance.stock: 
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, "Product added to cart")
        else:
            messages.warning(request, "No more stock available for this product")
    except Cart_items.DoesNotExist:
        if product_instance.stock > 0: 
            cart_item = Cart_items.objects.create(product=product_instance, cart=cart, quantity=1)
            cart_item.save()
            messages.success(request, "Product added to cart")
        else:
            messages.warning(request, "No stock available for this product")
    
    return redirect('cart')


def cartitems(request):
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        coupons = Coupon.objects.filter(is_active=True)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id = _cart_id(request))
        cart.save()
        
    
    cart_items = Cart_items.objects.filter(cart=cart).order_by('-added_time')
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    tax = round((total_price * 0.2),2)
    
    
    discount = 0
    coupon_code = request.session.get('coupon_code')
    request.session['original_price'] = total_price
    
    if coupon_code:
       try:
            coupon = Coupon.objects.get(code=coupon_code, is_active=True)
            discount = round(total_price * (round(coupon.discount) / 100), 2)
            request.session['coupon_discount'] = discount
       except Coupon.DoesNotExist:
            messages.error(request, "Invalid or expired coupon")
            request.session['coupon_code'] = None  # Remove invalid coupon

    final_price = round(total_price + tax - discount, 2)
    
    context = {
        'cart_items' : cart_items,
        'total_price': total_price,
        'tax': tax,
        'final_price': final_price,
        'coupons' : coupons,
        'discount': discount,
        'active_coupon':coupon_code
        
    }
    return render(request, 'store/cart.html', context)

def remove_cart(request, p_id):
    product_instance = product.objects.filter(id=p_id).first()  # Use .first() to get the first item or None
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_item = None  
    try:
        cart_item = Cart_items.objects.get(cart=cart, product=product_instance)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
        return redirect('cart')
    except Cart_items.DoesNotExist:
        return redirect('cart')

@login_required
def checkout(request):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_items = Cart_items.objects.filter(cart=cart)
    user = request.user
    delivery_address = Address.objects.filter(user=user)
    
    coupon_code = request.session.get('coupon_code')
    
    if coupon_code:
        coupon = Coupon.objects.get(code=coupon_code, is_active=True)
        coupon_discount = request.session.get('coupon_discount')
        original_price = request.session.get('original_price')
        print(coupon, coupon_code, coupon_discount)
        tax = round((original_price * 0.2), 2)
        final_price = original_price - coupon_discount + tax
    else:
        original_price = request.session.get('original_price')
        tax = round((original_price * 0.2), 2)
        final_price = original_price + tax
        coupon = None
        coupon_discount= None
        
    context = {
        'cart_item': cart_items,
        'addresses': delivery_address, 
        'coupon' : coupon,
        'coupon_discount' : coupon_discount,
        'original_price' : original_price,
        'final_price' : final_price,
        'tax': tax
    }

    if cart_items.exists():
        return render(request, 'store/checkout.html', context)
    else:
        messages.error(request, "Your cart is empty.")
        return redirect('cart')



def add_address(request):
    if request.method == 'POST':
        # Retrieve form data from POST request
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address_line_1 = request.POST.get('address_line_1')
        address_line_2 = request.POST.get('address_line_2')
        pincode = request.POST.get('pincode')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        address_type = request.POST.get('address_type')

        # Create Address object
        address = Address.objects.create(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address_line_1=address_line_1,
            address_line_2=address_line_2,
            pincode=pincode,
            city=city,
            state=state,
            country=country,
            address_type=address_type
        )

        # Save the address
        address.save()
        
        # Redirect the user back to the checkout page
        return redirect('checkout')



def cart_increase(request, increase_id):
    cart_item = Cart_items.objects.get(id=increase_id)
    if cart_item.quantity >= 5:
        messages.error(request, 'Maximum quantity per user has been reached')
    else:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

def cart_decrease(request, decrease_id):
    cart_item = Cart_items.objects.get(id=decrease_id)
    if cart_item.quantity <= 1:
        messages.error(request, 'Minimum quantity per user has been reached')
    else:
        cart_item.quantity -= 1
        cart_item.save()
    return redirect('cart')

@require_POST
def apply_coupon(request):
    coupon_code = request.POST.get('coupon_code')
    if coupon_code:
        # coupon = Coupon.objects.get(code=coupon_code, is_active=True)
        request.session['coupon_code'] = coupon_code
        messages.success(request, f"Coupon '{coupon_code}' applied successfully")
    else:
        messages.error(request, "No coupon to add")
    return redirect('cart')

def remove_coupon(request):
    if 'coupon_code' in request.session:
        del request.session['coupon_code']
        del request.session['coupon_discount']
        messages.success(request, "Coupon removed successfully")
    else:
        messages.error(request, "No coupon to remove")
    return redirect('cart')