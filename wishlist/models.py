from django.db import models
from store.models import product
from accounts.models import account

class Wishlist(models.Model):
    user = models.ForeignKey(account, on_delete=models.CASCADE, related_name='wishlists')
    product = models.ForeignKey(product, on_delete=models.CASCADE, related_name='wishlist_entries')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Wishlist of {self.user.first_name} - {self.product.product_name}"