from django.urls import include
from django.conf.urls import url

from dynamic_rest.routers import DynamicRouter

from dandy.content import views

app_name = 'content'

router = DynamicRouter()
router.register('articles', views.ArticleViewSet)
router.register_resource(views.ArticleViewSet)


urlpatterns = [
    url(r'^', include(router.urls))
]
