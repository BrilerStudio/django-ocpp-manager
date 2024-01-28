from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from djangoql.admin import DjangoQLSearchMixin

from utils.helpers import pretty_json_html
from . import models
from .forms import ChargePointAdminForm


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
        'charge_point_id',
        'description',
        'status',
        'manufacturer',
        'latitude',
        'longitude',
        'serial_number',
        'model',
        'location',
    )

    search_fields = (
        'id',
        'charge_point_id',
        'description',
        'status',
        'manufacturer',
        'latitude',
        'longitude',
        'serial_number',
        'comment',
        'model',
        'connectors',
        'location',
    )

    list_filter = (
        'id',
        'charge_point_id',
        'description',
        'status',
        'manufacturer',
        'latitude',
        'longitude',
        'serial_number',
        'comment',
        'model',
        'connectors',
        'location',
    )

    list_select_related = (
        'location',
    )

    list_display_links = (
        'id',
        'charge_point_id',
    )

    readonly_fields = (
        'id',
        'status',
        'connectors',
        'websocket_url',
    )

    fieldsets = (
        (
            _('General'),
            {
                'fields': (
                    'id',
                    'charge_point_id',
                    'status',
                    'connectors',
                    'location',
                    'websocket_url',
                ),
            },
        ),
        (
            _('Info'),
            {
                'fields': (
                    'description',
                    'manufacturer',
                    'latitude',
                    'longitude',
                    'serial_number',
                    'comment',
                    'model',
                ),
            },
        ),
        (
            _('Password'),
            {
                'fields': (
                    'password',
                ),
            },
        ),
    )
    form = ChargePointAdminForm


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

    list_select_related = (
        'charge_point',
    )

    list_display_links = (
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
                    'get_meter_value_raw',
                    'meter_stop',
                    'charge_point',
                ),
            },
        ),
    )

    @admin.display(description='Meter value raw')
    def get_meter_value_raw(self, obj: models.Transaction):
        if obj.meter_value_raw:
            return pretty_json_html(obj.meter_value_raw)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
