from django.apps import AppConfig


class ContentConfig(AppConfig):
    name = 'dandy.content'

    def ready(self):
        from . import signals
