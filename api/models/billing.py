from django.db import models
from api.models import Order


class Billing(models.Model):
    STATUS_CHOICE = (('Unpaid','Unpaid'),
                     ('Paid','Paid'))
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='billings')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20,default='Unpaid')
    received = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
