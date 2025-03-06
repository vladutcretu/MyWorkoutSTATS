# Django
from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self):
        """
        Method created to read signals.py, used to create muscle groups and
        exercises to newly registered accounts
        """
        import core.signals  # noqa: F401
