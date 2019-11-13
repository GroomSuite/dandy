from dynamic_rest.serializers import DynamicModelSerializer
from dynamic_rest.fields import DynamicRelationField
from rest_framework import serializers

from .models import Article, Image


class ImageSerializer(DynamicModelSerializer):
    class Meta:
        model = Image
        name = "image"
        fields = ("id", "image_file", "title", "url")


class ArticleSerializer(DynamicModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Article
        name = "article"
        fields = ("id", "label", "title", "publish_from",
                  "image", "lead_text", "url")

    def get_image(self, obj):
        image = obj.alter_image

        if not image:
            image = obj.main_image

        serialized = ImageSerializer(
            image, context={"request": self.context["request"]}
        )

        return serialized.data


class ArticleDetailSerializer(ArticleSerializer):
    class Meta:
        fields = ("id", "label", "title", "publish_from",
                  "main_image", "alter_image", "lead_text", "url")
