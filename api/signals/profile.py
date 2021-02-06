from django.db.models.signals import post_delete, post_save, post_init
from django.dispatch import receiver
from django.contrib.auth.models import User
from api.models import UserProfile


@receiver(post_delete, sender=User)
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created=None, *args, **kwargs):
    if created:
        profile = UserProfile.objects.filter(user=instance).exists()
        if not profile:
            UserProfile.objects.create(user=instance)