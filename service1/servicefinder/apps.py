# servicefinder/apps.py

from django.apps import AppConfig

class ServicefinderConfig(AppConfig):
    name = 'servicefinder'

    def ready(self):
        import servicefinder.signals  # Importing signals to ensure they are registered
