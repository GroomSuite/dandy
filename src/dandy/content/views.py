from dynamic_rest.viewsets import DynamicModelViewSet

from .serializers import ArticleSerializer, ImageSerializer, KeywordSerializer
from .models import Article, Image, Keyword


from rest_framework import viewsets


class ImageViewSet(DynamicModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class KeywordViewSet(DynamicModelViewSet):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer


class ArticleViewSet(DynamicModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
