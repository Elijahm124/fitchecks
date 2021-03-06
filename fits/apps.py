from django.apps import AppConfig


class FitsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fits'

    def ready(self):
        import fits.signals
