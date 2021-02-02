from django.contrib import admin
from api.models import UserProfile, Merchant, Product, Order
from api.admin.GenericModelAdmin import GenericModelAdmin
from api.admin.UserProfileAdmin import UserProfileAdmin
from api.admin.MerchantAdmin import MerchantAdmin
from api.admin.ProductAdmin import ProductAdmin
from api.admin.OrderAdmin import OrderAdmin

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Merchant, MerchantAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
