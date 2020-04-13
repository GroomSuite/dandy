from django.conf import settings
from appconf import AppConf


class ContentConf(AppConf):
    ARTICLE_SCHEMA = {
        'content': {
            'type': 'list'
        },
        'keywords': {
            'type': 'many',
            'model': 'content.Keyword'
        },
        'cover_image': {
            'type': 'one',
            'model': 'content.Image'
        },
        'section': {
            'type': 'one',
            'model': 'content.Section'
        }
    }
    TYPE_DEFAULTS = {
        'string': '',
        'int': 0,
        'float': 0.0,
        'datetime': None,
        'list': [],
        'dict': {},
        'one': None,
        'many': []
    }
