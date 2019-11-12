from dynamic_rest.viewsets import DynamicModelViewSet

from .serializers import ArticleSerializer
from .models import Article


class ArticleViewSet(DynamicModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
