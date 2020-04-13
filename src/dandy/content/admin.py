from django.conf import settings
from django.contrib import admin
from django.contrib.postgres import fields
from django.utils.safestring import mark_safe

from django_json_widget.widgets import JSONEditorWidget

from .models import Article, Section, Image, Keyword


class JSONFieldMixin():
    formfield_overrides = {
        fields.JSONField: {'widget': JSONEditorWidget},
    }


class ArticleAdmin(JSONFieldMixin, admin.ModelAdmin):
    list_display = [
        "title",
        "is_published",
        "created_on",
        "last_change",
    ]
    list_filter = ["is_published"]
    search_fields = ["title"]
    readonly_fields = ["created_on"]


admin.site.register(Article, ArticleAdmin)


class SectionAdmin(JSONFieldMixin, admin.ModelAdmin):
    list_display = ["name", "parent", "order", "id"]


admin.site.register(Section, SectionAdmin)


class ImageAdmin(JSONFieldMixin, admin.ModelAdmin):
    def image_preview(self, obj, max_width="512px"):
        if obj.image_file:
            return mark_safe(
                f'<img src="{settings.MEDIA_URL}{obj.image_file}" style="width: 100%; max-width: {max_width};" />'
            )
        else:
            return "No Image Found"

    def list_image_preview(self, obj):
        return self.image_preview(obj, "256px")

    image_preview.allow_tags = True

    list_display = ["calculated_name", "created_on",
                    "image_file", "list_image_preview"]
    search_fields = ["title", "image_file"]

    readonly_fields = ["image_preview", "created_on"]
    fields = [
        "image_file",
        "image_preview",
        "title",
        "description",
        "data",
        "created_on",
    ]


admin.site.register(Image, ImageAdmin)


class KeywordAdmin(JSONFieldMixin, admin.ModelAdmin):
    list_display = ["name", "created_on"]
    search_fields = ["name"]
    readonly_fields = ["created_on"]


admin.site.register(Keyword, KeywordAdmin)
