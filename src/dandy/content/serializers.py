from dynamic_rest.serializers import DynamicModelSerializer

from .models import Article


class ArticleSerializer(DynamicModelSerializer):
    class Meta:
        model = Article
        name = "article"
        fields = ("id", "label", "title", "publish_from")

    # location = DynamicRelationField('LocationSerializer')
    # groups = DynamicRelationField('GroupSerializer', many=True)
