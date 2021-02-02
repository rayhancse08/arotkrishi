from api.admin import GenericModelAdmin


class UserProfileAdmin(GenericModelAdmin):

    list_display = (
        'name', 'phone_number',)
    search_fields = ('phone_number',)