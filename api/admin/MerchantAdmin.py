from api.admin import GenericModelAdmin
from django.contrib import admin
from api import models


class MerchantPermissionInline(admin.StackedInline):
    model = models.MerchantPermission
    # form = OrderFlavorInlineForm
    extra = 0


class MerchantAdmin(GenericModelAdmin):
    inlines = (MerchantPermissionInline,)
    list_display = (
        'name', 'type', 'organization', 'phone_number', 'active', 'active_status_update_date',
        'trade_licence_expire_date', 'renewal_trade_licence', 'created')
    search_fields = ('name', 'phone_number',)
