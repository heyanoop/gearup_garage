from django.db import models
from django.utils import timezone
from categories.models import category
from store.models import product

# Create your models here.
class category_offer(models.Model):
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    discount = models.IntegerField()
    valid_from = models.DateTimeField(default=timezone.now)
    valid_until = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return str(self.category)
    
    def save(self, *args, **kwargs):
        if self.valid_until < timezone.now():
            self.is_active = False
        else:
            self.is_active = True
        
        super().save(*args, **kwargs)
        
        if not self.is_active:
            products_in_category = product.objects.filter(category=self.category)
            for prod in products_in_category:
                if prod.old_price:
                    prod.price = prod.old_price
                    prod.old_price = 0
                    prod.save()

class product_offer(models.Model):
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    discount = models.IntegerField()
    valid_from = models.DateTimeField(default=timezone.now)
    valid_until = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return str(self.product)
    
    def save(self, *args, **kwargs):
        if self.valid_until < timezone.now():
            self.is_active = False
        else:
            self.is_active = True
        
        super().save(*args, **kwargs)
        
        if not self.is_active:
            if self.product.old_price:
                self.product.price = self.product.old_price
                self.product.old_price = 0
                self.product.save()