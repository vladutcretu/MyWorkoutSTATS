from django.apps import AppConfig


class BackendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend'
    
    def ready(self):
        """Method created to read signals.py (used to create muscle groups and exercises to newly registered accounts)"""
        import backend.signals