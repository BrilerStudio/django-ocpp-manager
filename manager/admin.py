from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from djangoql.admin import DjangoQLSearchMixin

from . import models


@admin.register(models.Location)
class LocationAdmin(DjangoQLSearchMixin, admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'city',
        'address1',
        'address2',
        'comment',
    )

    search_fields = (
        'id',
        'name',
        'city',
        'address1',
        'address2',
        'comment',
    )

    list_filter = (
        'id',
        'name',
        'city',
        'address1',
        'address2',
        'comment',
    )

    readonly_fields = (
        'id',
    )

    fieldsets = (
        (
            _('General'),
            {
                'fields': (
                    'id',
                    'name',
                    'city',
                    'address1',
                    'address2',
                    'comment',
                ),
            },
        ),
    )


@admin.register(models.ChargePoint)
class ChargePointAdmin(DjangoQLSearchMixin, admin.ModelAdmin):
    list_display = (
        'id',
        'description',
        'status',
        'manufacturer',
        'latitude',
        'longitude',
        'serial_number',
        'comment',
        'model',
        'password',
        'connectors',
        'location',
    )

    search_fields = (
        'id',
        'description',
        'status',
        'manufacturer',
        'latitude',
        'longitude',
        'serial_number',
        'comment',
        'model',
        'password',
        'connectors',
        'location',
    )

    list_filter = (
        'id',
        'description',
        'status',
        'manufacturer',
        'latitude',
        'longitude',
        'serial_number',
        'comment',
        'model',
        'password',
        'connectors',
        'location',
    )

    readonly_fields = (
        'id',
        'status',
        'connectors',
    )

    fieldsets = (
        (
            _('General'),
            {
                'fields': (
                    'id',
                    'description',
                    'status',
                    'manufacturer',
                    'latitude',
                    'longitude',
                    'serial_number',
                    'comment',
                    'model',
                    'password',
                    'connectors',
                    'location',
                ),
            },
        ),
    )


@admin.register(models.Transaction)
class TransactionAdmin(DjangoQLSearchMixin, admin.ModelAdmin):
    list_display = (
        'transaction_id',
        'city',
        'vehicle',
        'address',
        'meter_start',
        'meter_stop',
        'charge_point',
    )

    search_fields = (
        'transaction_id',
        'city',
        'vehicle',
        'address',
        'meter_start',
        'meter_stop',
        'charge_point',
    )

    list_filter = (
        'transaction_id',
        'city',
        'vehicle',
        'address',
        'meter_start',
        'meter_stop',
        'charge_point',
    )

    readonly_fields = (
        'city',
        'vehicle',
        'address',
        'meter_start',
        'meter_stop',
        'charge_point',
        'transaction_id',
    )

    fieldsets = (
        (
            _('General'),
            {
                'fields': (
                    'transaction_id',
                    'city',
                    'vehicle',
                    'address',
                    'meter_start',
                    'meter_stop',
                    'charge_point',
                ),
            },
        ),
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
