from django.db import models
from api.models import Order


class Billing(models.Model):
    STATUS_CHOICE = (('Unpaid', 'Unpaid'),
                     ('Paid', 'Paid'),
                     ('Partially Paid', 'Partially Paid'))
    PAYMENT_TYPE = (('Full', 'Full'),
                    ('Partial', 'Partial'))
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='billings')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='Unpaid')
    payment_date = models.DateField(null=True, blank=True)
    bank_name = models.CharField(max_length=100, null=True, blank=True)
    branch_name = models.CharField(max_length=100, null=True, blank=True)
    check_no = models.CharField(max_length=100, null=True, blank=True)
    check_date = models.DateField(null=True, blank=True)
    payment_type = models.CharField(choices=PAYMENT_TYPE, default='Full',max_length=20)
    partial_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True
                                         )
    attachment = models.ImageField(null=True, blank=True)
    received = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
