from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Image, Article, Keyword


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_published',
                    'publish_from', 'created_on', 'last_change']
    raw_id_fields = ['main_image', 'alter_image']


admin.site.register(Article, ArticleAdmin)


class ImageAdmin(admin.ModelAdmin):

    def image_preview(self, obj):
        if obj.image_file:
            return mark_safe(f'<img src="{settings.MEDIA_URL}{obj.image_file}" style="width: 100%; max-width: 256px;" />')
        else:
            return 'No Image Found'

    image_preview.allow_tags = True

    list_display = ['calculated_name',
                    'created_on', 'image_file', 'image_preview']


admin.site.register(Image, ImageAdmin)
