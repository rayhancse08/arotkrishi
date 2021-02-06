from django.db.models.signals import post_save, post_delete
from api.models import OrderItem
from django.dispatch import receiver


@receiver(post_save, sender=OrderItem)
@receiver(post_delete, sender=OrderItem)
def update_purchase_total_price(sender, instance, created=None, *args, **kwargs):
    order = instance.order
    order.save()
