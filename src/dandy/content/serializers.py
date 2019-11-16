from dynamic_rest.serializers import DynamicModelSerializer
from dynamic_rest.fields import DynamicRelationField
from rest_framework import serializers

from .models import Article, Image, Keyword


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


class ArticleSerializer(DynamicModelSerializer):
    class Meta:
        model = Article
        name = "article"
        fields = [
            "id", "label", "title", "publish_from",
            "main_image", "alter_image", "lead_text",
            "keywords",
            "url"
        ]

    main_image = DynamicRelationField('ImageSerializer', embed=True)
    alter_image = DynamicRelationField('ImageSerializer', embed=True)
    keywords = DynamicRelationField('KeywordSerializer', many=True)
