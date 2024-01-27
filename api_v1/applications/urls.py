from django.urls import include, path

from .users import urls as users_urls

urlpatterns = [
    path('users/', include(users_urls)),
]
