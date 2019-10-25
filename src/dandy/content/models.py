from django.db import models
from django.utils.translation import ugettext_lazy as _


class Article(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=511)
    label = models.CharField(verbose_name=_('Label'), max_length=255,
                             default='', blank=True)
    lead_text = models.TextField(verbose_name=_(
        'Lead text'), default='', blank=True)
    content = models.TextField(verbose_name=_(
        'Content'), default='', blank=True)
