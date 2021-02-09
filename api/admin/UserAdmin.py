from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from api import models
from django.contrib import admin


class ProfileInline(admin.StackedInline):
    # readonly_fields = (
    #     'facebook', 'accountkit', 'otp', 'otp_created', 'wrong_otp_count', 'api_request_count', 'last_request_time')
    model = models.UserProfile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    @staticmethod
    def name(obj):
        return obj.profile.name

    @staticmethod
    def phone_number(obj):
        return obj.profile.phone_number

    @staticmethod
    def email_address(obj):
        return obj.profile.email

    inlines = (ProfileInline,)

    list_display = ('id', 'username', 'name', 'phone_number', 'email_address')
