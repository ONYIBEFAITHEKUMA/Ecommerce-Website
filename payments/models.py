
from django.db import models
from django.conf import settings
from store.models import Product

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    reference = models.CharField(max_length=200, unique=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f'Payment {self.reference} by {self.user}'
