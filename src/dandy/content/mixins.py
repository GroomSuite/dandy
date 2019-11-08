from django.db import models
from django.utils.translation import ugettext_lazy as _


class CreatedDateMixin(models.Model):
    created_on = models.DateTimeField(
        verbose_name=_('Created on'), auto_now_add=True)
    last_change = models.DateTimeField(
        verbose_name=_('Last change'), auto_now=True)
    # TODO: last change by identificator?

    class Meta:
        abstract = True

    @property
    def has_been_modified(self):
        return self.created_on != self.last_change
