from rest_framework import permissions, viewsets
from rest_framework.response import Response

from . import serializers


def choices_to_list(cs):
    return [{'id': i[0], 'value': i[1], 'name': i[1]} for i in cs]


class EnumViewSet(viewsets.GenericViewSet):
    pagination_class = None
    serializer_class = serializers.EnumSerializer
    permission_classes = [
        permissions.IsAdminUser,
    ]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'results': serializer.data, 'count': len(serializer.data)})
