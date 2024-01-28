from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

from api_v1.filters import ReactSearchFilter
from api_v1.mixins import ApiV1ViewMixin
from api_v1.paginations import AdminPageNumberPagination
from manager.models import ChargePoint, Location, Transaction
from utils.drf_helpers import create_handler
from . import serializers


class ChargePointViewSet(ApiV1ViewMixin, viewsets.ModelViewSet):
    pagination_class = AdminPageNumberPagination
    queryset = ChargePoint.objects.all().select_related('location')
    serializer_class = serializers.ChargePointSerializer
    filter_backends = [DjangoFilterBackend, ReactSearchFilter, filters.OrderingFilter]
    search_fields = [
        'id',
        'code',
        'description',
        'status',
        'manufacturer',
        'latitude',
        'longitude',
        'serial_number',
        'comment',
        'model',
        'location',
    ]
    filterset_fields = [
        'code',
        'description',
        'status',
        'manufacturer',
        'latitude',
        'longitude',
        'serial_number',
        'comment',
        'model',
        'location',
    ]
    ordering_fields = [
        'code',
        'description',
        'status',
        'manufacturer',
        'latitude',
        'longitude',
        'serial_number',
        'comment',
        'model',
        'location',
    ]
    ordering = [
        'code',
        'description',
        'status',
        'manufacturer',
        'latitude',
        'longitude',
        'serial_number',
        'comment',
        'model',
        'location',
    ]

    @action(detail=True, methods=['post'], serializer_class=serializers.ChargePointVerifyPasswordSerializer)
    def verify_password(self, request, *args, **kwargs):
        context = self.get_serializer_context()
        context['charge_point'] = self.get_object()

        return create_handler(self, request, *args, **kwargs, context=context)


class LocationViewSet(ApiV1ViewMixin, viewsets.ModelViewSet):
    pagination_class = AdminPageNumberPagination
    queryset = Location.objects.all()
    serializer_class = serializers.LocationSerializer
    filter_backends = [DjangoFilterBackend, ReactSearchFilter, filters.OrderingFilter]
    search_fields = [
        'id',
        'name',
        'city',
        'address1',
        'address2',
        'comment',
    ]
    filterset_fields = [
        'id',
        'name',
        'city',
        'address1',
        'address2',
        'comment',
    ]
    ordering_fields = [
        'id',
        'name',
        'city',
        'address1',
        'address2',
        'comment',
    ]
    ordering = [
        'id',
        'name',
        'city',
        'address1',
        'address2',
        'comment',
    ]


class TransactionViewSet(ApiV1ViewMixin, viewsets.ReadOnlyModelViewSet):
    pagination_class = AdminPageNumberPagination
    queryset = Transaction.objects.all().select_related('charge_point', 'charge_point__location')
    serializer_class = serializers.TransactionSerializer
    filter_backends = [DjangoFilterBackend, ReactSearchFilter, filters.OrderingFilter]
    search_fields = [
        'transaction_id',
        'city',
        'vehicle',
        'address',
        'meter_start',
        'meter_stop',
        'charge_point',
    ]
    filterset_fields = [
        'transaction_id',
        'city',
        'vehicle',
        'address',
        'meter_start',
        'meter_stop',
        'charge_point',
    ]
    ordering_fields = [
        'transaction_id',
        'city',
        'vehicle',
        'address',
        'meter_start',
        'meter_stop',
        'charge_point',
    ]
    ordering = [
        'transaction_id',
        'city',
        'vehicle',
        'address',
        'meter_start',
        'meter_stop',
        'charge_point_id',
    ]

    @action(detail=True, methods=['post'], serializer_class=serializers.TransactionSerializer)
    def approve(self, request, *args, **kwargs):
        raise ValidationError('Not implemented yet')

    @action(detail=True, methods=['post'], serializer_class=serializers.TransactionSerializer)
    def reject(self, request, *args, **kwargs):
        raise ValidationError('Not implemented yet')

    @action(detail=True, methods=['post'], serializer_class=serializers.TransactionSerializer)
    def stop(self, request, *args, **kwargs):
        raise ValidationError('Not implemented yet')
