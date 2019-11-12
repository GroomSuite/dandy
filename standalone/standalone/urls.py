from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


from dandy.content.urls import urlpatterns as content_urlpatterns


api_urlpatterns = [
    url('auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('content/', include(content_urlpatterns))
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urlpatterns)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
