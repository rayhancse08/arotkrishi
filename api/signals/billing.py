from django.db.models.signals import post_save, post_delete
from api.models import Payment
from django.dispatch import receiver


@receiver(post_save, sender=Payment)
@receiver(post_delete, sender=Payment)
def update_paid_amount(sender, instance, created=None, *args, **kwargs):
    billing = instance.billing
    billing.save()