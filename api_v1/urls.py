from django.urls import include, path

from .applications import urls

app_name = 'api_v1'

urlpatterns = [
    path('', include(urls.urlpatterns)),
]
