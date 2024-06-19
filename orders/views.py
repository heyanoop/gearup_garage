from django.shortcuts import redirect, render, get_object_or_404, HttpResponse
from django.contrib import messages
from cart.models import Cart, Cart_items
from .models import Order, OrderProduct, Payment
from cart.models import Address
from cart.views import _cart_id
from django.db.models import F
from django.contrib.auth.decorators import login_required
from coupon.models import Coupon
import razorpay 
from user_dashboard.models import wallet
from django.template.loader import get_template
from xhtml2pdf import pisa

def non_admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return render(request, 'error.html', {'message': 'You are not authorized to access this page.'})
    return wrapper


from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings

from django.utils.decorators import method_decorator

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def place_order(request):
    if request.method == 'POST':
        address_id = request.POST.get('address')
        payment_method = request.POST.get('payment_method')
        selected_address = Address.objects.get(id=address_id)
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = Cart_items.objects.filter(cart=cart)
        
        
        coupon_code = request.session.get('coupon_code')
        original_price = request.session.get('original_price')
        tax = original_price * 0.2
        
        if original_price > 1000 and payment_method == 'cash on Delivery':
            messages.error(request, 'Orders above 1000 are not allowed for cash on delivery')
            return redirect('cart')
        
        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code, is_active=True)
                coupon_discount = request.session.get('coupon_discount')
                final_price = original_price - coupon_discount + tax
            except Coupon.DoesNotExist:
                messages.error(request, 'Invalid or inactive coupon code')
                return redirect('cart')
        else:
            final_price = original_price + tax
            coupon_discount = None
            coupon = None

        for cart_item in cart_items:
            if cart_item.quantity > cart_item.product.stock:
                messages.error(request, f"Sorry, {cart_item.product.product_name} is out of stock.")
                return redirect('cart')

        # Create order
        order = Order.objects.create(
            user=request.user,
            first_name=selected_address.first_name,
            last_name=selected_address.last_name,
            phone=selected_address.phone,
            email=selected_address.email,
            address_line_1=selected_address.address_line_1,
            address_line_2=selected_address.address_line_2,
            pincode=selected_address.pincode,
            country=selected_address.country,
            state=selected_address.state,
            city=selected_address.city,
            ip=request.META.get('REMOTE_ADDR'),
            address_type=selected_address.address_type,
            payment_method=payment_method,
            order_total=final_price,
            original_price=original_price,
            discount_price=coupon_discount,
            tax=tax,
            is_ordered=True,
            coupon_used=coupon,
        )
        request.session['order_id'] = order.id

        # Handle payment
        if payment_method == 'wallet':
            try:
                wallet_pay = wallet.objects.get(user=request.user)
            except wallet.DoesNotExist:
            # Create a new wallet with a default balance of zero
                wallet_pay = wallet.objects.create(user=request.user, amount=0)

            if wallet_pay.amount < order.order_total:
                messages.error(request, "Insufficient funds in wallet")
                return redirect('cart')
            else:
                wallet_pay.amount -= order.order_total
                wallet_pay.save()
                payment = Payment.objects.create(
                    user=request.user,
                    payment_method=payment_method,
                    amount_paid=final_price,
                    status='completed'
                )
                order.payment = payment
                order.save()

        elif payment_method == 'debit_card':
            if not order.razorpay_order_id:
                order_currency = 'INR'
                notes = {'order-type': "basic order from the website"}
                receipt_maker = str(order.id)
                razorpay_order = razorpay_client.order.create(dict(
                    amount=int(order.order_total * 100),
                    currency=order_currency,
                    notes=notes,
                    receipt=receipt_maker,
                    payment_capture='1'
                ))
                order.razorpay_order_id = razorpay_order['id']
                order.save()
            
            total_amount = order.order_total * 100
            callback_url = 'http://' + str(get_current_site(request)) + "/payment_gateway/handlerequest/"

            context = {
                'order': order,
                'razorpay_order_id': order.razorpay_order_id,
                'order_id': order.id,
                'total_amount': total_amount,
                'total_price': total_amount,
                'razorpay_merchant_id': settings.RAZORPAY_KEY_ID,
                'callback_url': callback_url
            }
            return render(request, 'store/razorpay_gateway.html', context)

        # Create order products and decrease product quantity
        for cart_item in cart_items:
            cart_item.product.stock -= cart_item.quantity
            cart_item.product.save()

            OrderProduct.objects.create(
                order=order,
                user=request.user,
                product=cart_item.product,
                quantity=cart_item.quantity,
                product_price=cart_item.product.price,
                ordered=True
            )

        # Delete cart items after order is placed
        cart_items.delete()

        return render(request, 'store/order_placed.html')
    else:
        return render(request, 'error.html', {'message': 'Invalid request method'})
    
def generate_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_products = OrderProduct.objects.filter(order=order)
    

    template_path = 'user/invoice.html'
    context = {
        'order': order,
        'order_products': order_products
    }
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice_{}.pdf"'.format(order_id)
    
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
       html, dest=response
    )
    
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response