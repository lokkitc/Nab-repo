from django.apps import AppConfig

class UserConfig(AppConfig):
    verbose_name = 'Пользователи'
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'

