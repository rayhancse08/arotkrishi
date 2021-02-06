from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


@receiver(post_delete, sender=User)
@receiver(post_save, sender=User)
def update_user_token(sender, instance, created=None, *args, **kwargs):
    if created:
        Token.objects.create(user=instance)