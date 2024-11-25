from django.apps import AppConfig


class UserCmsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_cms'

    def ready(self):
        import user_cms.signals