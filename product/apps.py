from django.apps import AppConfig


class ProductConfig(AppConfig):
    verbose_name = 'Товары'
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'product'
