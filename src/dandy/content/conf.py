from django.conf import settings
from appconf import AppConf


class ContentConf(AppConf):
    DEFAULT_ARTICLE_DATA = {
        'content': [],
        'keywords': [],
        'cover_image': None,
        'section': None
    }
