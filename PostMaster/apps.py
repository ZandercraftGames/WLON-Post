from django.apps import AppConfig


class PostmasterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'PostMaster'

    def ready(self):
        # Import all signals from the signals module
        from . import signals
