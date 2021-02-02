from api.admin import GenericModelAdmin


class ProductAdmin(GenericModelAdmin):
    list_display = (
        'name', 'product_code', 'last_unit_rate', 'unit_rate', 'unit', 'created')
    search_fields = ('name',)
