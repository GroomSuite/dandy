from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Article, Section, Image, Keyword


class ArticleAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "is_published",
        "section",
        "publish_from",
        "created_on",
        "last_change",
    ]
    list_filter = ["is_published", "section"]
    raw_id_fields = ["section", "main_image", "alter_image", "keywords"]
    search_fields = ["title", "label", "lead_text"]
    readonly_fields = ["created_on"]


admin.site.register(Article, ArticleAdmin)


class SectionAdmin(admin.ModelAdmin):
    list_display = ["name", "parent", "order", "id"]


admin.site.register(Section, SectionAdmin)


class ImageAdmin(admin.ModelAdmin):
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


class KeywordAdmin(admin.ModelAdmin):
    list_display = ["name", "created_on"]
    search_fields = ["name"]
    readonly_fields = ["created_on"]


admin.site.register(Keyword, KeywordAdmin)
