# Django
from django.apps import AppConfig
import sys


class FitnessConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "fitness"

    def ready(self):
        """
        Method created to read signals.py from api directory, used to
        invalidate caches from API views
        """
        if "test" not in sys.argv:
            # Method is not executed on command: python manage.py test
            import fitness.api.signals  # noqa: F401
