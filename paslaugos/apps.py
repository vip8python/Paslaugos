from django.apps import AppConfig


class PaslaugosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'paslaugos'
    verbose_name = 'Meniu'

    def ready(self):
        from .signals import create_profile, save_profile