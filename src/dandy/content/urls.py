from django.urls import include
from django.conf.urls import url

from dynamic_rest.routers import DynamicRouter

from .views import ArticleViewSet, ImageViewSet, KeywordViewSet, SectionViewSet

app_name = 'content'

router = DynamicRouter()

router.register('article', ArticleViewSet)
router.register('image', ImageViewSet)
router.register('keyword', KeywordViewSet)
router.register('section', SectionViewSet)


urlpatterns = [
    url(r'^', include(router.urls))
]
