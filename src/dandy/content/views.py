from dynamic_rest.viewsets import DynamicModelViewSet

from .serializers import ArticleSerializer, ArticleDetailSerializer, ImageSerializer
from .models import Article, Image


from rest_framework import viewsets


class MultiSerializerMixin(viewsets.ModelViewSet):
    serializer_classes = {}

    def get_serializer_class(self):
        return self.serializer_classes.get(
            self.action,
            self.serializer_class
        )


class ArticleViewSet(MultiSerializerMixin, DynamicModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    serializer_classes = {
        'detail':  ArticleDetailSerializer
    }


class ImageViewSet(DynamicModelViewSet):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()
