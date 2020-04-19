from django.db.models.signals import pre_save
from django.dispatch import receiver

# TODO: move this somewhere else (module?)
from django.apps import apps

from .conf import settings
from .exceptions import (
    ModelDoesNotExistError,
    UnsuportedRelationTypeError,
    InstanceDoesNotExistError,
    IdValueNotFoundError
)
from .serializers import serializers_mapping

# TODO: move this somewhere else (module?)


def validate_model_name(name, definition):
    model_name = definition.get('model')

    try:
        apps.get_model(model_name)
    except (ValueError, LookupError):
        raise ModelDoesNotExistError(
            f'Cannot find model "{model_name}" for field "{name}"')


# TODO: move this somewhere else (module?)
def validate_relation_type(name, definition):
    relation_types = settings.CONTENT_RELATION_TYPES
    field_relation_type = definition.get('type')

    if field_relation_type not in relation_types:
        raise UnsuportedRelationTypeError(
            f'Unsupported relation type "{field_relation_type}" for field "{name}"'
        )


# TODO: move this somewhere else (module?)
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


def get_related_id(value):
    if isinstance(value, int):
        return value
    elif isinstance(value, dict) and 'id' in value and isinstance(value['id'], int):
        return value['id']
    else:
        raise IdValueNotFoundError(
            'Passed value must be integer type or dict with "id" key-value pair! '
            f'"{value}" cannot be handled properly.'
        )


def get_serialized_data(obj):
    serializer_class = serializers_mapping.get(obj._meta.model)

    return serializer_class(obj, context={'request': None}, include_fields='*').data


def get_related_serialized_data(value, model_class):
    related_id = get_related_id(value)
    related_obj = model_class.objects.filter(id=related_id).first()

    if related_obj:
        return get_serialized_data(related_obj)
    else:
        raise InstanceDoesNotExistError(
            f'{model_class} instance with id {related_id} does not exist!')


def get_related_serialized_data_many(value_list, model_class):
    if isinstance(value_list, list):
        related_data_list = []

        for item in value_list:
            related_data = get_related_serialized_data(
                item, model_class)
            related_data_list.append(related_data)

        return related_data_list
    else:
        raise IdValueNotFoundError(
            'Passed value must be list of integer type values or dicts with "id" key-value pair! '
            f'"{value_list}" cannot be handled properly.'
        )


# TODO: move logic inside somewhere else (module?)
@receiver(pre_save, sender='content.Article')
def serialize_related_objects(sender, instance, **kwargs):
    relation_definitions = get_relation_definitions()

    for key, definition in relation_definitions.items():
        model_class = apps.get_model(definition.get('model'))
        value = instance.data.get(key)
        default_value = settings.CONTENT_TYPE_DEFAULTS.get(
            definition.get('type'))
        relation_type = definition.get('type')

        if value != default_value:
            if relation_type == 'one':
                instance.data[key] = get_related_serialized_data(
                    value, model_class)
            elif relation_type == 'many':
                instance.data[key] = get_related_serialized_data_many(
                    value, model_class)
