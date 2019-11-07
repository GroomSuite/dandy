from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .mixins import CreatedDateMixin


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


class Article(CreatedDateMixin):
    title = models.CharField(verbose_name=_("Title"), max_length=511)
    label = models.CharField(
        verbose_name=_("Label"), max_length=255, default="", blank=True
    )
    lead_text = models.TextField(verbose_name=_(
        "Lead text"), default="", blank=True)
    main_image = models.ForeignKey(
        "content.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="image",
    )
    alter_image = models.ForeignKey(
        "content.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="alter_image",
    )
    content = models.TextField(verbose_name=_(
        "Content"), default="", blank=True)
    keywords = models.ManyToManyField(
        "content.Keyword", verbose_name=_("Keywords"))
    publish_from = models.DateTimeField(
        verbose_name=_("Publish from"), null=True, blank=True, db_index=True
    )
    publish_to = models.DateTimeField(
        verbose_name=_("Publish to"), null=True, blank=True
    )
    is_published = models.BooleanField(
        verbose_name=_("Is published"), default=False)
    data = JSONField(default=dict, blank=True, null=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.id}:{self.title}"
