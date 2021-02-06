from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        # noinspection PyUnresolvedReferences
        import api.signals
