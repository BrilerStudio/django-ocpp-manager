from django.apps import AppConfig


class ApiAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api_admin'

    def ready(self):
        import api_admin.receivers  # noqa
