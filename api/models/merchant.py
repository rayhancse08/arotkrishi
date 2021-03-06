from django.contrib.auth.models import User
from django.db import models


class Merchant(models.Model):
    MERCHANT_TYPE = ((1, 'Buyer'),
                     (2, 'Seller'))
    name = models.CharField(max_length=255, null=True)
    logo = models.ImageField(null=True, blank=True)
    type = models.IntegerField(choices=MERCHANT_TYPE)
    organization = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(null=True, blank=True)
    address = models.TextField()
    nid = models.FileField(null=True, blank=True)
    trade_licence = models.FileField(null=True, blank=True)
    tin_certificate = models.FileField(null=True, blank=True)
    trade_licence_expire_date = models.DateField(null=True, blank=True)
    renewal_trade_licence = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    active_status_update_date = models.DateField(null=True, blank=True)
    md_contact_details = models.CharField(max_length=300, null=True, blank=True)
    agreement = models.FileField(null=True, blank=True)
    agreement_date = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name


class MerchantPermission(models.Model):
    USER_TYPE = (('procurement', 'Procurement'),
                 ('store manager', 'Store Manager'),
                 ('accounts', 'Accounts'),)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='merchant_user_permissions', null=True,
                             blank=True)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='merchant_permissions', null=True,
                                 blank=True)
    user_type = models.CharField(choices=USER_TYPE, max_length=20, default='procurement')
    active = models.BooleanField(default=True)
    owner = models.BooleanField(default=False)
    create_permission = models.BooleanField(default=False)
    read_permission = models.BooleanField(default=False)
    update_permission = models.BooleanField(default=False)
    delete_permission = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.user.profile.name
