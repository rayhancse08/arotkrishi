from django.contrib import admin
from django.contrib.auth.models import User
from api.models import UserProfile, Merchant, Product, Order,Billing,Payment
from api.admin.GenericModelAdmin import GenericModelAdmin
from api.admin.UserProfileAdmin import UserProfileAdmin
from api.admin.MerchantAdmin import MerchantAdmin
from api.admin.ProductAdmin import ProductAdmin
from api.admin.OrderAdmin import OrderAdmin
from api.admin.UserAdmin import UserAdmin

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Merchant, MerchantAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Billing)
admin.site.register(Payment)