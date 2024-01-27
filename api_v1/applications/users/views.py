from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets

from api_v1.filters import ReactSearchFilter
from api_v1.paginations import AdminPageNumberPagination
from . import serializers


class UserViewSet(viewsets.ModelViewSet):
    pagination_class = AdminPageNumberPagination
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAdminUser, permissions.DjangoModelPermissions]
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
