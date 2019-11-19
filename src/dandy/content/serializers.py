from dynamic_rest.serializers import DynamicModelSerializer
from dynamic_rest.fields import DynamicRelationField
from rest_framework import serializers

from .models import Article, Image, Keyword, Section


class ImageSerializer(DynamicModelSerializer):
    class Meta:
        model = Image
        name = "image"
        fields = [
            "id", "image_file", "title", "url",
            "data"
        ]
        deferred_fields = ["data"]


class KeywordSerializer(DynamicModelSerializer):
    class Meta:
        model = Keyword
        name = "keyword"
        fields = [
            "id", "name", "url",
            "data"
        ]
        deferred_fields = ["data"]


class SectionSerializer(DynamicModelSerializer):
    class Meta:
        model = Section
        name = "section"
        fields = [
            "id", "name", "url",
            "order", "parent",
            "data",
        ]
        deferred_fields = ["data", "parent"]

    parent = serializers.SerializerMethodField()

    def get_parent(self, obj):
        parent = obj.parent

        if parent:
            return SectionSerializer(parent, context={'request': self.context['request']}).data


class ArticleSerializer(DynamicModelSerializer):
    class Meta:
        model = Article
        name = "article"
        fields = [
            "id", "label", "title", "publish_from", "url",
            "main_image", "alter_image", "lead_text",
            "keywords", "section",
            "data",
            "content", "publish_to", "is_published"
        ]
        deferred_fields = ["data", "content", "publish_to", "is_published"]

    main_image = DynamicRelationField('ImageSerializer', embed=True)
    alter_image = DynamicRelationField('ImageSerializer', embed=True)
    keywords = DynamicRelationField('KeywordSerializer', many=True)
    section = DynamicRelationField('SectionSerializer', embed=True)
