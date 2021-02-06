from api.admin import GenericModelAdmin
from django.contrib import admin
from api import models


class OrderItemInline(admin.StackedInline):
    model = models.OrderItem
    # form = OrderFlavorInlineForm
    extra = 0


class OrderAdmin(GenericModelAdmin):
    inlines = (OrderItemInline,)
    list_display = (
        'order_no', 'order_date', 'delivery_date', 'buyer', 'created_by', 'total_amount', 'created')
    search_fields = ('order_no',)
