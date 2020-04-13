from .conf import settings


def get_default_article_data():
    schema_definition = settings.CONTENT_ARTICLE_SCHEMA
    type_defaults = settings.CONTENT_TYPE_DEFAULTS

    default_data = {}

    for key, field_definition in schema_definition.items():
        field_type = field_definition.get('type', 'string')

        default_data[key] = type_defaults.get(field_type, '')

    return default_data
