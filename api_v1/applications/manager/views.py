from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

from api_v1.filters import ReactSearchFilter
from api_v1.mixins import ApiV1ViewMixin
from api_v1.paginations import AdminPageNumberPagination
from manager.models import ChargePoint, Location, Transaction
from utils.drf_helpers import create_handler
from . import serializers


class ChargePointViewSet(ApiV1ViewMixin, viewsets.ModelViewSet):
    lookup_field = 'charge_point_id'
    pagination_class = AdminPageNumberPagination
    queryset = ChargePoint.objects.all().select_related('location')
    serializer_class = serializers.ChargePointSerializer
    filter_backends = [DjangoFilterBackend, ReactSearchFilter, filters.OrderingFilter]
    search_fields = [
        'id',
        'charge_point_id',
        'description',
        'is_enabled',
        'manufacturer',
        'latitude',
        'longitude',
        'serial_number',
        'model',
        'location',
        'created_at',
        'updated_at',
    ]
    filterset_fields = [
        'id',
        'charge_point_id',
        'description',
        'is_enabled',
        'manufacturer',
        'latitude',
        'longitude',
        'serial_number',
        'model',
        'location',
        'created_at',
        'updated_at',
    ]
    ordering_fields = [
        'id',
        'charge_point_id',
        'description',
        'is_enabled',
        'manufacturer',
        'latitude',
        'longitude',
        'serial_number',
        'model',
        'location',
        'created_at',
        'updated_at',
    ]
    ordering = [
        'id',
        'charge_point_id',
        'description',
        'is_enabled',
        'manufacturer',
        'latitude',
        'longitude',
        'serial_number',
        'model',
        'location',
        'created_at',
        'updated_at',
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
        'description',
        'created_at',
        'updated_at',
    ]
    filterset_fields = [
        'id',
        'name',
        'city',
        'address1',
        'address2',
        'description',
        'created_at',
        'updated_at',
    ]
    ordering_fields = [
        'id',
        'name',
        'city',
        'address1',
        'address2',
        'description',
        'created_at',
        'updated_at',
    ]
    ordering = [
        'id',
        'name',
        'city',
        'address1',
        'address2',
        'description',
        'created_at',
        'updated_at',
    ]


class TransactionViewSet(ApiV1ViewMixin, viewsets.ReadOnlyModelViewSet, mixins.CreateModelMixin):
    pagination_class = AdminPageNumberPagination
    queryset = Transaction.objects.all().select_related('charge_point', 'charge_point__location')
    serializer_class = serializers.TransactionSerializer
    filter_backends = [DjangoFilterBackend, ReactSearchFilter, filters.OrderingFilter]
    search_fields = [
        'transaction_id',
        'tag_id',
        'city',
        'vehicle',
        'address',
        'meter_start',
        'meter_stop',
        'charge_point',
        'connector_id',
        'external_id',
        'start_date',
        'end_date',
    ]
    filterset_fields = [
        'transaction_id',
        'tag_id',
        'city',
        'vehicle',
        'address',
        'meter_start',
        'meter_stop',
        'charge_point',
        'connector_id',
        'external_id',
        'start_date',
        'end_date',
    ]
    ordering_fields = [
        'transaction_id',
        'tag_id',
        'city',
        'vehicle',
        'address',
        'meter_start',
        'meter_stop',
        'charge_point',
        'connector_id',
        'external_id',
        'start_date',
        'end_date',
    ]

    ordering = [
        'id',
        'transaction_id',
        'tag_id',
        'city',
        'vehicle',
        'address',
        'meter_start',
        'meter_stop',
        'charge_point',
        'connector_id',
        'external_id',
        'start_date',
        'end_date',
    ]

    @action(detail=True, methods=['post'], serializer_class=serializers.TransactionSerializer)
    def stop(self, request, *args, **kwargs):
        raise ValidationError('Not implemented yet')
