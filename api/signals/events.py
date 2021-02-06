import django.dispatch
user_post_save = django.dispatch.Signal(providing_args=["instance", "created"])