from django.db import models
from store.models import product
from accounts.models import account

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length= 250, blank= True)
    date_added  = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return self.cart_id
    
class Cart_items(models.Model):
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete= models.CASCADE)
    quantity  = models.IntegerField()
    is_active = models.BooleanField(default= True)
    added_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.product
    

class Address(models.Model):
    user = models.ForeignKey(account, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    pincode = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    address_type = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.address_line_1}, {self.city}, {self.country}"