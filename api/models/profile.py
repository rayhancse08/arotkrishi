from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(
        # help_text="eg: +8801*******, +88 is important",
        max_length=20,
        blank=True,
        null=True,
        unique=True
    )
    email = models.EmailField(null=True, blank=True)
    profile_picture = models.ImageField(
        null=True,
        blank=True
    )
    address = models.CharField(null=True, blank=True, max_length=255)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
