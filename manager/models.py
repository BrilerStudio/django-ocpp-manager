from enum import StrEnum

from django.contrib.auth.hashers import check_password
from django.db import models
from django.utils.translation import gettext_lazy as _
from ocpp.v16.enums import ChargePointStatus

from app.settings import WEBSOCKETS_URL
from manager.defaults import tagid_generator


class Location(models.Model):
    class Meta:
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')

    name = models.CharField(
        max_length=48,
        unique=True
    )

    city = models.CharField(
        max_length=48
    )

    address1 = models.CharField(
        max_length=256,
    )

    address2 = models.CharField(
        max_length=256,
        null=True,
        blank=True
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        editable=False,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        blank=True,
        editable=False,
    )

    def __str__(self):
        return f'Location: {self.name}, {self.city}, {self.id}'


class ChargePoint(models.Model):
    class Meta:
        verbose_name = _('Charge Point')
        verbose_name_plural = _('Charge Points')

    charge_point_id = models.CharField(
        max_length=256,
        unique=True,
        null=False,
        blank=False,
    )

    is_enabled = models.BooleanField(
        default=True,
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=50,
        choices=[(tag, tag.value) for tag in ChargePointStatus],
        default=ChargePointStatus.unavailable,
    )

    manufacturer = models.CharField(
        max_length=256,
        null=True,
        blank=True,
    )

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    serial_number = models.CharField(
        max_length=48,
        unique=True,
        null=True,
        blank=True,
    )

    model = models.CharField(
        max_length=256,
        null=True,
        blank=True,
    )

    password_hash = models.CharField(
        max_length=256,
        null=True,
        blank=True
    )

    connectors = models.JSONField(
        default=dict,
        editable=False,
    )

    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name='charge_points',
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        editable=False,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        blank=True,
        editable=False,
    )

    last_seen_at = models.DateTimeField(
        null=True,
        blank=True,
        editable=False,
    )

    @property
    def connectors_count(self):
        return len(self.connectors)

    def is_available(self, connector_id: int = 0):
        if connector_id:
            connector = self.connectors.get(str(connector_id), {})
            return connector.get('status') == ChargePointStatus.available
        return self.status == ChargePointStatus.available

    def check_password(self, password):
        return not self.password_hash or check_password(password, self.password_hash)

    @property
    def websocket_url(self):
        return f'{WEBSOCKETS_URL}/{self.charge_point_id}'

    def __str__(self):
        return f'ChargePoint {self.id} {self.charge_point_id} {self.status}'


class TransactionStatus(StrEnum):
    initialized = 'initialized'
    requested = 'requested'
    started = 'started'
    stopping = 'stopping'
    stopped = 'stopped'


class Transaction(models.Model):
    class Meta:
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')

    transaction_id = models.AutoField(
        primary_key=True,
    )

    tag_id = models.CharField(
        max_length=20,
        default=tagid_generator,
        help_text='One time tag id only for this charge point and connector.',
    )

    city = models.CharField(
        max_length=48,
        null=True,
        blank=True,
    )

    vehicle = models.CharField(
        max_length=256,
        null=True,
        blank=True,
    )

    address = models.CharField(
        max_length=256,
        null=True,
        blank=True,
    )

    meter_start = models.IntegerField(
        null=True,
        blank=True,
    )

    meter_stop = models.IntegerField(
        null=True,
        blank=True,
    )

    meter_value_raw = models.JSONField(
        default=dict,
        editable=False,
        null=True,
        blank=True,
    )

    charge_point = models.ForeignKey(
        ChargePoint,
        on_delete=models.CASCADE,
        related_name='transactions',
    )

    connector_id = models.IntegerField(
        default=1,
    )

    external_id = models.CharField(
        max_length=256,
        null=True,
        blank=True,
    )

    start_date = models.DateTimeField(
        auto_now_add=True
    )

    end_date = models.DateTimeField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=50,
        choices=[(tag, tag.value) for tag in TransactionStatus],
        default=TransactionStatus.initialized,
    )

    def __str__(self):
        return f'Transaction {self.transaction_id}'
