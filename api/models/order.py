from django.db import models
from api.models.product import Product
from api.models.merchant import Merchant
from django.contrib.auth.models import User
import uuid


class Order(models.Model):
    ORDER_STATUS = ((1, 'Pending'),
                    (2, 'Confirmed'),
                    (3, 'Processing'),
                    (4, 'Shipping'),
                    (5, 'Delivered'))
    order_no = models.CharField(max_length=20, null=True, blank=True)
    order_date = models.DateField()
    delivery_date = models.DateField()
    buyer = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='orders')
    status = models.IntegerField(choices=ORDER_STATUS, default=1)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(
        null=True,
        blank=True,
        max_digits=10,
        decimal_places=2, )

    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    @property
    def is_new(self):
        if self.id:
            return False
        return True

    def save(self, *args, **kwargs):
        if self.is_new:
            self.set_defaults_before_saving()
        if self.order_items.exists():
            self.total_amount = sum(self.order_items.values_list('amount', flat=True))
        # self.total_amount = (self.sub_total_amount or 0) - (self.discount or 0)

        super(Order, self).save(*args, **kwargs)

    def set_defaults_before_saving(self):
        self.order_no = self.get_order_no()

    def get_order_no(self):
        buyer_name = self.buyer.name[:2].upper()

        order_day = self.order_date.strftime("%d")
        order_month = self.order_date.strftime("%m")
        order_year = self.order_date.strftime("%y")
        return buyer_name + order_day + order_month + order_year + uuid.uuid4().hex[:2].upper()

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
