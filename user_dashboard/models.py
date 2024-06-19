from django.db import models
from accounts.models import account

class wallet(models.Model):
    user = models.ForeignKey(account, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username} wallet"