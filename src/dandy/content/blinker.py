from django.apps import apps

from .conf import settings
from .exceptions import (
    ModelDoesNotExistError,
    UnsuportedRelationTypeError,
    InstanceDoesNotExistError,
    IdValueNotFoundError
)
from .serializers import serializers_mapping


class Blinker():
    model_schema_map = {
        'content.Article': settings.CONTENT_ARTICLE_SCHEMA
    }
    content_type_defaults = settings.CONTENT_TYPE_DEFAULTS
    relation_types = settings.CONTENT_RELATION_TYPES

    def __init__(self, model_namespace, *args, **kwargs):
        self.model_namespace = model_namespace

    def validate_model_name(self, name, definition):
        model_name = definition.get('model')

        try:
            apps.get_model(model_name)
        except (ValueError, LookupError):
            raise ModelDoesNotExistError(
                f'Cannot find model "{model_name}" for field "{name}"')

    def validate_relation_type(self, name, definition):
        field_relation_type = definition.get('type')

        if field_relation_type not in self.relation_types:
            raise UnsuportedRelationTypeError(
                f'Unsupported relation type "{field_relation_type}" for field "{name}"'
            )

    def get_related_id(self, value):
        if isinstance(value, int):
            return value
        elif isinstance(value, dict) and 'id' in value and isinstance(value['id'], int):
            return value['id']
        else:
            raise IdValueNotFoundError(
                'Passed value must be integer type or dict with "id" key-value pair! '
                f'"{value}" cannot be handled properly.'
            )

    def get_serialized_data(self, obj):
        serializer_class = serializers_mapping.get(obj._meta.model)

        return serializer_class(obj, context={'request': None}, include_fields='*').data

    def get_related_serialized_data(self, value, model_class):
        related_id = self.get_related_id(value)
        related_obj = model_class.objects.filter(id=related_id).first()

        if related_obj:
            return self.get_serialized_data(related_obj), related_id
        else:
            raise InstanceDoesNotExistError(
                f'{model_class} instance with id {related_id} does not exist!')

    def get_related_serialized_data_many(self, value_list, model_class):
        if isinstance(value_list, list):
            related_data_list = []
            related_ids = []

            for item in value_list:
                related_data, related_id = self.get_related_serialized_data(
                    item, model_class)

                if related_id not in related_ids:
                    related_ids.append(related_id)
                    related_data_list.append(related_data)

            return related_data_list, related_ids
        else:
            raise IdValueNotFoundError(
                'Passed value must be list of integer type values or dicts with "id" key-value pair! '
                f'"{value_list}" cannot be handled properly.'
            )

    def get_relation_definitions(self):
        schema_definition = self.model_schema_map[self.model_namespace]

        relation_definitions = {}

        for key, field_definition in schema_definition.items():
            field_relation_type = field_definition.get('type')
            model_name = field_definition.get('model')

            if field_relation_type and model_name:
                self.validate_model_name(key, field_definition)
                self.validate_relation_type(key, field_definition)

                relation_definitions[key] = field_definition

        return relation_definitions

    def focus(self, instance):
        relation_definitions = self.get_relation_definitions()

        for key, definition in relation_definitions.items():
            model_class = apps.get_model(definition.get('model'))
            value = instance.data.get(key)
            default_value = self.content_type_defaults.get(
                definition.get('type'))
            relation_type = definition.get('type')

            if value != default_value:
                if relation_type == 'one':
                    serialize_method = self.get_related_serialized_data
                elif relation_type == 'many':
                    serialize_method = self.get_related_serialized_data_many

                instance.data[key], related_id_s = serialize_method(
                    value, model_class)

        return instance
