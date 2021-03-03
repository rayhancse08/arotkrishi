from django.db.models.signals import post_save, post_delete
from api.models import OrderItem, Order, Billing
from django.dispatch import receiver


@receiver(post_save, sender=OrderItem)
@receiver(post_delete, sender=OrderItem)
def update_purchase_total_price(sender, instance, created=None, *args, **kwargs):
    order = instance.order
    order.save()


@receiver(post_save, sender=Order)
@receiver(post_delete, sender=Order)
def add_billing(sender, instance, created=None, *args, **kwargs):
    if instance.status == 'Confirmed' and not instance.billings.exists():
        Billing.objects.create(order=instance, amount=instance.total_amount)
