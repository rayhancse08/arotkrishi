from reversion.admin import VersionAdmin


class GenericModelAdmin(VersionAdmin):
    save_on_top = True

    def __init__(self, *args, **kwargs):
        super(GenericModelAdmin, self).__init__(*args, **kwargs)

        # DON'T remove!! used with dal
        self.form.admin_site = self.admin_site