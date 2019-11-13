from django.urls import include
from django.conf.urls import url

from dynamic_rest.routers import DynamicRouter

from .views import ArticleViewSet, ImageViewSet

app_name = 'content'

router = DynamicRouter()

router.register('article', ArticleViewSet)
router.register('image', ImageViewSet)


urlpatterns = [
    url(r'^', include(router.urls))
]
