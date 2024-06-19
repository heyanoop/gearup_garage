from django.db import models
from categories.models import category
from django.urls import reverse
from django.apps import apps

class product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    stock = models.IntegerField(blank=True, null = True)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)
    old_price = models.IntegerField(null = True, blank = True)
    is_active = models.BooleanField(default=True)
    
     
    def get_product_offer(self):
        ProductOffer = apps.get_model('offer_management', 'product_offer')
        product_offers = ProductOffer.objects.filter(product=self, is_active=True).first()
        return product_offers.discount if product_offers else 0
    
    def get_category_discount(self):
       CategoryOffer = apps.get_model('offer_management', 'category_offer')
       category_offers = CategoryOffer.objects.filter(category=self.category, is_active=True).first()
       return category_offers.discount if category_offers else 0
    
    def get_url(self):
        return reverse('product_details', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name


class ProductImage(models.Model):
    product = models.ForeignKey(product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/products')

    def __str__(self):
        return f"{self.product.product_name} Image"
    
class Product_Variation(models.Model):
    variation_name = models.CharField(max_length=50)
    item = models.ForeignKey(product, related_name='variant', on_delete=models.CASCADE)
    stock = models.IntegerField(default=0)