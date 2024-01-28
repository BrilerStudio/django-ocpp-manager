from django.urls import include, path

from .manager import urls as manager_urls

urlpatterns = [
    path('manager/', include(manager_urls)),
]
