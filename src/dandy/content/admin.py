from django.contrib import admin

from .models import Image, Article, Keyword


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_published',
                    'publish_from', 'created_on', 'last_change']
    raw_id_fields = ['main_image', 'alter_image']


admin.site.register(Article, ArticleAdmin)


class ImageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Image, ImageAdmin)
