from django.apps import AppConfig

class AdminCmsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admin_cms'

    def ready(self):
        import admin_cms.signals