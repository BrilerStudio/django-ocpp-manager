from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from api_v1.filters import ReactSearchFilter
from api_v1.mixins import ApiV1ViewMixin
from api_v1.paginations import AdminPageNumberPagination
from . import serializers


class UserViewSet(ApiV1ViewMixin, viewsets.ModelViewSet):
    pagination_class = AdminPageNumberPagination
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    filter_backends = [DjangoFilterBackend, ReactSearchFilter, filters.OrderingFilter]
    search_fields = [
        'username',
        'first_name',
        'last_name',
        'email',
    ]
    filterset_fields = [
        'id',
    ]
    ordering_fields = [
        'id',
        'username',
        'email',
    ]
    ordering = [
        'id',
    ]
