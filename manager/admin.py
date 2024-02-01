from admin_auto_filters.filters import AutocompleteFilterFactory
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
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
        'description',
        'created_at',
        'updated_at',
    )

    search_fields = (
        'id',
        'name',
        'city',
        'address1',
        'address2',
        'description',
        'created_at',
        'updated_at',
    )

    list_filter = (
        'id',
        'name',
        'city',
        'address1',
        'address2',
        'description',
        'created_at',
        'updated_at',
    )

    readonly_fields = (
        'id',
        'created_at',
        'updated_at',
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
                    'description',
                    'created_at',
                    'updated_at',
                ),
            },
        ),
    )


@admin.register(models.ChargePoint)
class ChargePointAdmin(DjangoQLSearchMixin, admin.ModelAdmin):
    list_display = (
        'id',
        'charge_point_id',
        'is_enabled',
        'status',
        'manufacturer',
        'serial_number',
        'model',
        'location',
        'created_at',
        'updated_at',
    )

    search_fields = (
        'id',
        'charge_point_id',
        'is_enabled',
        'description',
        'status',
        'manufacturer',
        'latitude',
        'longitude',
        'serial_number',
        'model',
        'connectors',
        'location',
        'created_at',
        'updated_at',
    )

    list_filter = (
        'id',
        'charge_point_id',
        'is_enabled',
        'description',
        'status',
        'manufacturer',
        'latitude',
        'longitude',
        'serial_number',
        'model',
        'connectors',
        AutocompleteFilterFactory('Location', 'location'),
        'created_at',
        'updated_at',
    )

    autocomplete_fields = (
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
        'created_at',
        'updated_at',
        'get_meter_value_raw',
        'connectors_count',
    )

    fieldsets = (
        (
            _('General'),
            {
                'fields': (
                    'id',
                    'charge_point_id',
                    'is_enabled',
                    'status',
                    'get_meter_value_raw',
                    'connectors_count',
                    'location',
                    'websocket_url',
                    'created_at',
                    'updated_at',
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

    @admin.display(description='Connectors')
    def get_meter_value_raw(self, obj: models.ChargePoint):
        if obj.connectors:
            return pretty_json_html(obj.connectors)

    actions = ['remote_start_transaction']

    @admin.action(description='Remote start transaction')
    def remote_start_transaction(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(
                request, 'Please select exactly one charge point to start remote transaction.', level='error'
            )
        else:
            charge_point = queryset.first()
            charge_point_url = reverse(
                'manager:remote-start-transaction'
            )
            charge_point_url = f'{charge_point_url}?charge_point={charge_point.pk}'
            return HttpResponseRedirect(charge_point_url)


@admin.register(models.Transaction)
class TransactionAdmin(DjangoQLSearchMixin, admin.ModelAdmin):
    list_display = (
        'transaction_id',
        'tag_id',
        'status',
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
    )

    search_fields = (
        'transaction_id',
        'tag_id',
        'status',
        'city',
        'vehicle',
        'address',
        'meter_start',
        'meter_stop',
        'meter_value_raw'
        'charge_point',
        'connector_id',
        'external_id',
        'start_date',
        'end_date',
    )

    list_filter = (
        'transaction_id',
        'tag_id',
        'status',
        AutocompleteFilterFactory('Charge Point', 'charge_point'),
        'city',
        'vehicle',
        'address',
        'meter_start',
        'meter_stop',
        'connector_id',
        'external_id',
        'start_date',
        'end_date',
    )

    autocomplete_fields = (
        'charge_point',
    )

    list_display_links = (
        'transaction_id',
        'tag_id',
    )

    readonly_fields = (
        'transaction_id',
        'tag_id',
        'status',
        'meter_start',
        'meter_value_raw',
        'meter_stop',
        'charge_point',
        'connector_id',
        'start_date',
        'end_date',
        'get_meter_value_raw',
    )

    fieldsets = (
        (
            _('General'),
            {
                'fields': (
                    'transaction_id',
                    'tag_id',
                    'status',
                    'meter_start',
                    'meter_stop',
                    'get_meter_value_raw',
                    'charge_point',
                    'connector_id',
                    'start_date',
                    'end_date',
                ),
            },
        ),
        (
            _('Info'),
            {
                'fields': (
                    'city',
                    'vehicle',
                    'address',
                    'external_id',
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
