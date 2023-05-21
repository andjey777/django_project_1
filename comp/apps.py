from django.apps import AppConfig


class CompConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'comp'
    verbose_name = 'Component'
    verbose_name_plural = 'Components'
