from django.db import models
from accounts.models import account
from cart.models import Address
from store.models import product
from coupon.models import Coupon
# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey(account, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.IntegerField()
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.payment_id
    
class Order(models.Model):
    STATUS = (
        ('PENDING', 'pending'),
        ('CONFIRMED', 'confirmed'),
        ('SHIPPED', 'shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'cancelled'),
        ('RETURN_REQUESTED', 'return_requested'),
        ('RETURN_ACCEPTED', 'return_accepted'),
        ('RETURN_REJECTED', 'return_rejected'),
        ('RETURNED', 'returned')
        
                    
    )
    user = models.ForeignKey(account, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50, blank=True)
    pincode = models.IntegerField(default=000)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    order_note = models.CharField(max_length=100, blank=True)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS, default='PENDING')
    ip = models.CharField(blank=True, max_length=20)
    is_cancelled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    address_type = models.CharField(max_length= 20)
    is_ordered=models.BooleanField(default=False)
    original_price = models.IntegerField(default=0)
    discount_price = models.IntegerField(default=0, null=True, blank=True)
    coupon_used = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    payment_status = models.CharField(max_length=20, default='PENDING')
    payment_method = models.CharField(max_length=20, default='CASH ON DELIVERY') 
    razorpay_order_id = models.CharField(max_length=200, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=200, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=200, null=True, blank=True)
    return_note =  models.CharField(max_length=250, null=True, blank=True)
    
    def __str__(self):
        return self.first_name
    

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(account, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=True)
    is_cancelled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.product.product_name
