from django.apps import AppConfig


class ExcercisesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'excercises'

    def ready(self):
        import excercises.signals