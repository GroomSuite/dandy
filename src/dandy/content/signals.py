from django.db.models.signals import pre_save
from django.dispatch import receiver

from .blinker import Blinker


@receiver(pre_save, sender='content.Article')
def serialize_related_objects(sender, instance, **kwargs):
    blinker = Blinker('content.Article')
    blinker.focus(instance)
