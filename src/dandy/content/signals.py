from django.db.models.signals import pre_save
from django.dispatch import receiver

from .conf import settings

from django.apps import apps

from .exceptions import ModelDoesNotExistError, UnsuportedRelationTypeError


def validate_model_name(name, definition):
    model_name = definition.get('model')

    try:
        apps.get_model(model_name)
    except (ValueError, LookupError):
        raise ModelDoesNotExistError(
            f'Cannot find model "{model_name}" for field "{name}"')


def validate_relation_type(name, definition):
    relation_types = settings.CONTENT_RELATION_TYPES
    field_relation_type = definition.get('type')

    if field_relation_type not in relation_types:
        raise UnsuportedRelationTypeError(
            f'Unsupported relation type "{field_relation_type}" for field "{name}"'
        )


def get_relation_definitions():
    schema_definition = settings.CONTENT_ARTICLE_SCHEMA

    relation_definitions = {}

    for key, field_definition in schema_definition.items():
        field_relation_type = field_definition.get('type')
        model_name = field_definition.get('model')

        if field_relation_type and model_name:
            validate_model_name(key, field_definition)
            validate_relation_type(key, field_definition)

            relation_definitions[key] = field_definition

    return relation_definitions


@receiver(pre_save, sender='content.Article')
def serialize_related_objects(sender, instance, **kwargs):
    relation_definitions = get_relation_definitions()

    for key, definition in relation_definitions.items():
        model_class = apps.get_model(definition.get('model'))
        value = instance.data.get(key)
        default_value = settings.CONTENT_TYPE_DEFAULTS.get(
            definition.get('type'))

        if value != default_value:
            print(model_class.objects.filter(id=value).first())
