from django.urls import include, path

from . import views
from .applications import urls

app_name = 'api_admin'

urlpatterns = [
    path('', include(urls.urlpatterns)),
    path('permissions', views.PermissionsView.as_view(), name='api-permissions'),
    path('csrf', views.CsrfView.as_view(), name='api-csrf'),
]
