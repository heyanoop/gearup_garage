
from django.shortcuts import render, redirect, get_object_or_404
import razorpay
from django.conf import settings

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
from django.views.decorators.csrf import csrf_exempt
from cart.models import Cart, Cart_items
from accounts.models import account
from django.contrib.sites.shortcuts import get_current_site
from orders.models import OrderProduct, Payment,Order
from cart.views import _cart_id

# Create your views here.

@csrf_exempt
def handlerequest(request):
    if request.method == 'POST':
        try:
            payment_id = request.POST.get('razorpay_payment_id','')
            order_id = request.POST.get('razorpay_order_id','')
            signature = request.POST.get('razorpay_signature','')

          
            params_dict = { 
            'razorpay_order_id': order_id, 
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature,
            }
            try:
                order_db = Order.objects.get(razorpay_order_id=order_id)
            except:
                order_id_session = request.session.get('order_id',1)
               
                return redirect('razorpay_success')
            
            order_db.razorpay_payment_id = payment_id
            order_db.razorpay_signature = signature
            order_db.save()

            result = razorpay_client.utility.verify_payment_signature(params_dict)
            

            
            if result:
                amount = order_db.order_total  #we have to pass in paisa
                
                try:
                    
                    # razorpay_client.payment.capture(payment_id, amount)
                    order_db.payment_status= 'Success'
                    order_db.save()
                    
                    return redirect('razorpay_success')
                except:
                    
                    order_db.payment_status= 'Failure'
                    order_db.save()
                    
                    return redirect('razorpay_success')
            else:
                order_db.payment_status = 'Failure'
                order_db.save()
                
            return redirect('razorpay_success')
        except:
            
            order_db.payment_status = 'Failure'
            order_db.save()
            
            order_id_session = request.session.get('order_id', 1)
            
            return redirect('razorpay_success')

def cart_id(request):
    cart_id= request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id

def razorpay_success(request):
    user_id = request.session.get('user_id')  # Use get method to avoid KeyError
    user = None  # Initialize user to None

    if user_id is not None:  # Check if user_id exists
        user = get_object_or_404(account, pk=user_id)
    order_id_session = request.session.get('order_id')

    order = Order.objects.get(id = order_id_session)
    if order_id_session == 1:
        order.payment_status= 'Failure'
        order.save()
       
    
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_items = Cart_items.objects.filter(cart=cart) 
        
    for cart_item in cart_items:
        # Decrease product quantity
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
    if 'coupon_code' in request.session:
        del request.session['coupon_discount']
        del request.session['original_price']
        del request.session['coupon_code']
    
    return render(request, 'store/order_placed.html')


# RETRY PAYMENT======================================================
def retry_payment(request,id):
    order = Order.objects.get(id = id)
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
    callback_url = 'http://' + str(get_current_site(request)) + "/payment_gateway/handlerequest_retry/"
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


@csrf_exempt
def handlerequest_retry(request):
    if request.method == 'POST':
        try:
            payment_id = request.POST.get('razorpay_payment_id','')
            order_id = request.POST.get('razorpay_order_id','')
            signature = request.POST.get('razorpay_signature','')

            
            params_dict = { 
            'razorpay_order_id': order_id, 
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature,
            }
            try:
                order_db = Order.objects.get(razorpay_order_id=order_id)
            except:
                order_id_session = request.session.get('order_id',1)
                
                return redirect('razorpay_success__retry')
           
            order_db.razorpay_payment_id = payment_id
            order_db.razorpay_signature = signature
            order_db.save()

            result = razorpay_client.utility.verify_payment_signature(params_dict)
        

            
            if result:
                amount = order_db.order_total  #we have to pass in paisa
               
                
                try:
                   
                    # razorpay_client.payment.capture(payment_id, amount)
                    order_db.payment_status= 'Success'
                    order_db.save()
                    
                    return redirect('razorpay_success__retry')
                except:
                    
                    order_db.payment_status= 'Failure'
                    order_db.save()
                    
                    return redirect('razorpay_success__retry')
            else:
                order_db.payment_status = 'Failure'
                order_db.save()
              

            return redirect('razorpay_success__retry')
        except:
            
            order_db.payment_status = 'Failure'
            order_db.save()
           
            order_id_session = request.session.get('order_id', 1)
           
            return redirect('razorpay_success__retry')



def razorpay_success__retry(request):
    user_id = request.session.get('user_id')  # Use get method to avoid KeyError
    user = None  # Initialize user to None

    if user_id is not None:  # Check if user_id exists
        user = get_object_or_404(account, pk=user_id)
    order_id_session = request.session.get('order_id')
    
    order = Order.objects.get(id = order_id_session)
    if order_id_session == 1:
        order.payment_status= 'Failure'
        order.save()
       

    return render(request, 'store/order_placed.html')