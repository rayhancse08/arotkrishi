from django.db import models
from api.models import Order
from django.contrib.auth.models import User


class Billing(models.Model):
    STATUS_CHOICE = (('Unpaid', 'Unpaid'),
                     ('Paid', 'Paid'),
                     ('Partially Paid', 'Partially Paid'))

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='billing', primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICE, max_length=20, default='Unpaid')
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)


class Payment(models.Model):
    PAYMENT_TYPE = (('Full', 'Full'),
                    ('Partial', 'Partial'))
    billing = models.ForeignKey(Billing, on_delete=models.CASCADE, related_name='payments')
    payment_date = models.DateField(null=True, blank=True)
    bank_name = models.CharField(max_length=100, null=True, blank=True)
    branch_name = models.CharField(max_length=100, null=True, blank=True)
    check_no = models.CharField(max_length=100, null=True, blank=True)
    check_date = models.DateField(null=True, blank=True)
    payment_type = models.CharField(choices=PAYMENT_TYPE, default='Full', max_length=20)
    partial_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    attachment = models.ImageField(null=True, blank=True)
    received = models.BooleanField(default=False)
    paid_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='billings', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
