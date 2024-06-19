from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import account
from cart.models import Address
from orders.models import OrderProduct, Order,Payment
from store.models import product
from user_dashboard.models import wallet
from django.contrib.auth import authenticate, logout
import re

def regular_user_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('home')  # Or any other redirect you prefer
    return _wrapped_view_func

@login_required
@regular_user_required
def dashboard(request):
    user = request.user
  
    try:
        wal = wallet.objects.get(user=user)
    except wallet.DoesNotExist:
            wal= wallet(user=user, amount=0)
    print(wal.amount)
    context = {
        'wallet_bal': wal.amount,
        
    }
    return render(request, 'user/dashboard.html', context)

@login_required
@regular_user_required
def address_management(request):
    user = request.user
    addresses = Address.objects.filter(user=user)
    context = {
        'addresses': addresses,
        
    }
    return render(request, 'user/address_management.html', context)

@login_required
@regular_user_required
def order_management(request): 
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'all_orders': orders
    }
    return render(request, 'user/myorder.html', context)

@login_required
@regular_user_required
def order_details(request, order_id):
    single_order = OrderProduct.objects.filter(order_id=order_id)
    order_address = Order.objects.get(id=order_id)
    coupon = order_address.coupon_used.discount if order_address.coupon_used else 0
    coupon_discount = order_address.original_price *(coupon/100)
    
    context ={
        'single_order' : single_order,
        'address' : order_address,
    
    
    }
    return render(request, 'user/order_details.html', context)

@login_required
@regular_user_required
def confirm_cancel(request, id):
    single_order = Order.objects.get(id=id)
    context = {
        'single_order':single_order,

    }
    return render(request, 'user/confirm_cancel.html', context)


# @login_required
# @regular_user_required
# def cancel_order(request, id):
#     order = get_object_or_404(Order, id=id)
#     order_product = OrderProduct.objects.filter(order=order)
    
    
#     if order.user != request.user:
#         return redirect('home')
    
#     order.status = 'CANCELLED'
#     order.is_cancelled = True
#     order.save()
    
#     for product in order_product:
#         product.is_cancelled = True
#         product.product.stock += product.quantity
#         product.save()
#         product.product.save()

#     messages.success(request, 'Your order has been canceled.')
#     return redirect('myorders')

@login_required
@regular_user_required
def cancel_order(request, id):
    order = get_object_or_404(Order, id=id)
    order_products = OrderProduct.objects.filter(order=order)
    
    if order.user != request.user:
        return redirect('home')
    
    # Update order status to 'CANCELLED'
    order.status = 'CANCELLED'
    order.is_cancelled = True
    order.save()
    
    # Update order products
    for order_product in order_products:
        order_product.is_cancelled = True
        order_product.product.stock += order_product.quantity
        order_product.save()
        order_product.product.save()
    
    # Retrieve payment information for the order
    
    # Check if the payment method is a debit card and credit the wallet
    if order.payment_method.lower() == 'debit_card':
        try:
            wal = wallet.objects.get(user=order.user)
        except wallet.DoesNotExist:
            wal= wallet(user=order.user, amount=0)
        
        wal.amount += order.order_total
        wal.save()
    
    messages.success(request, 'Your order has been canceled.')
    return redirect('myorders')

def request_return(request, id):
    order = get_object_or_404(Order, id=id)
    if request.method == 'POST':
       reason = request.POST.get('reason')
        # Update order status to 'RETURN' and save the return note
       order.status = 'RETURN_REQUESTED'
       order.return_note = reason
       order.save()
       messages.success(request, 'Your return request has been submitted successfully.')
       return redirect('myorders')  # Redirect to an appropriate view after processing

    return render(request, 'user/request_return.html')
   


@login_required
@regular_user_required
def edit_address(request, id):
    address = get_object_or_404(Address, pk=id)
    
    if request.method == 'POST':
        address_id = request.POST.get('selected_address')
        # Update address fields based on form data
        address.first_name = request.POST.get('first_name')
        address.last_name = request.POST.get('last_name')
        address.email = request.POST.get('email')
        address.phone = request.POST.get('phone')
        address.address_line_1 = request.POST.get('address_line_1')
        address.address_line_2 = request.POST.get('address_line_2')
        address.pincode = request.POST.get('pincode')
        address.city = request.POST.get('city')
        address.state = request.POST.get('state')
        address.country = request.POST.get('country')
        address.address_type = request.POST.get('address_type')
        
        # Save the updated address
        address.save()
        
        return redirect('manage_address')
    
    return render(request, 'user/edit_address.html', {'address': address})

def delete_address(request, id):
    address = get_object_or_404(Address, pk=id)
    address.delete()
    return redirect('manage_address')


def edit_profile(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
         
        user = request.user
        user.first_name = first_name
        user.last_name = last_name

        user.phone_number = phone_number
        user.save()

        messages.success(request, 'Your profile has been updated successfully.')
        return redirect('edit_profile')

    return render(request, 'user/edit_profile.html')

def change_password(request):
    if request.method == 'POST':
        user = request.user
        
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        
        if not validate_password_complexity(new_password):
            messages.error(request, 'New password must contain at least 8 characters, including at least one letter, one number, and one special character')
            return redirect('change_password')

        if authenticate(username=user.email, password=current_password):
            user.set_password(new_password)
            user.save()
            
            logout(request)
            messages.success(request, 'Password changed successfully. Please login with your new password.')
            return redirect('login')
        else:
            messages.error(request, 'Incorrect password. Please try again.')
    
    return render(request, 'user/change_password.html')

def validate_password_complexity(password):
    pattern = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
    if re.match(pattern, password):
        return True
    else:
        return False
 
