from django.db import models
from api.models.product import Product
from api.models.merchant import Merchant
from django.contrib.auth.models import User


class Order(models.Model):
    order_no = models.CharField(max_length=20,null=True,blank=True)
    order_date = models.DateField()
    delivery_date = models.DateField()
    buyer = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='orders')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(
        null=True,
        blank=True,
        max_digits=10,
        decimal_places=2, )

    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def save(self, *args, **kwargs):
        if self.order_items.exists():
            self.sub_total_amount = sum(self.order_items.values_list('amount', flat=True))
        # self.total_amount = (self.sub_total_amount or 0) - (self.discount or 0)

        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return self.buyer.name

    class Meta:
        ordering = ["-created"]
        verbose_name_plural = "Orders"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items', null=True,
                                blank=True)
    quantity = models.DecimalField(
        null=True,
        blank=True,
        max_digits=10,
        decimal_places=2, )
    unit = models.CharField(max_length=20, blank=True, null=True)
    price = models.DecimalField(
        null=True,
        blank=True,
        max_digits=10,
        decimal_places=2, )
    amount = models.DecimalField(
        null=True,
        blank=True,
        max_digits=10,
        decimal_places=2, )
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def save(self, *args, **kwargs):
        self.amount = self.get_amount()
        super(OrderItem, self).save(*args, **kwargs)

    def get_amount(self):
        return self.quantity * self.price

    def __str__(self):
        return self.product.name

    class Meta:
        ordering = ["-created"]
