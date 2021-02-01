from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200)
    product_code = models.CharField(max_length=50, null=True, blank=True)
    last_unit_rate = models.DecimalField(
        null=True,
        blank=True,
        max_digits=10,
        decimal_places=2)
    unit_rate = models.DecimalField(
        null=True,
        blank=True,
        max_digits=10,
        decimal_places=2)
    unit = models.CharField(max_length=20, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
