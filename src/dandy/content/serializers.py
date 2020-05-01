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
            "id", "title", "url",
            "data",
            "is_published"
        ]
        deferred_fields = ["data", "is_published"]


serializers_mapping = {
    Article: ArticleSerializer,
    Section: SectionSerializer,
    Keyword: KeywordSerializer,
    Image: ImageSerializer
}
