from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .mixins import CreatedDateMixin
from .utils import get_default_article_data


class Image(CreatedDateMixin):
    image_file = models.ImageField(
        verbose_name=_("Image"), max_length=500, upload_to="upload"
    )
    title = models.CharField(
        verbose_name=_("Title"), blank=True, null=True, max_length=350
    )
    description = models.TextField(
        verbose_name=_("Description"), default="", blank=True
    )
    data = JSONField(default=dict, blank=True, null=True)

    def __str__(self):
        return f"{self.id}:{self.calculated_name}"

    @property
    def calculated_name(self):
        return self.title if self.title else self.image_file.name


class Keyword(CreatedDateMixin):
    name = models.CharField(
        verbose_name=_("Name"), max_length=100, db_index=True, unique=True
    )
    data = JSONField(default=dict, blank=True, null=True)

    def __str__(self):
        return f"{self.id}:{self.name}"

    def save(self, *args, **kwargs):
        self.name = self.name.lower()

        return super().save(*args, **kwargs)


class Section(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=100)
    parent = models.ForeignKey(
        "content.Section",
        verbose_name=_("Parent section"),
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="subsections",
    )
    order = models.PositiveIntegerField(verbose_name=_('Order'), default=0)
    data = JSONField(default=dict, blank=True, null=True)

    def __str__(self):
        full_name = f"{self.parent.name} - {self.name}" if self.parent else self.name

        return f"{self.id}:{full_name}"


class Article(CreatedDateMixin):
    title = models.CharField(verbose_name=_("Title"), max_length=511)
    is_published = models.BooleanField(
        verbose_name=_("Is published"), default=False)
    data = JSONField(default=get_default_article_data)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.id}:{self.title}"
