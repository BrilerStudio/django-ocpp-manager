from django.contrib.auth.hashers import check_password
from django.db import models
from django.utils.translation import gettext_lazy as _
from ocpp.v16.enums import ChargePointStatus

from app.settings import WEBSOCKETS_URL


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
        max_length=48
    )

    address2 = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    comment = models.TextField(
        max_length=200,
        null=True,
        blank=True
    )

    def __str__(self):
        return f'Location: {self.name}, {self.city}, {self.id}'


class ChargePoint(models.Model):
    class Meta:
        verbose_name = _('Charge Point')
        verbose_name_plural = _('Charge Points')

    code = models.CharField(
        max_length=256,
        unique=True,
        null=False,
        blank=False,
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
        max_length=48,
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

    comment = models.TextField(
        null=True,
        blank=True,
    )

    model = models.CharField(
        max_length=48,
        null=True,
        blank=True,
    )

    password_hash = models.CharField(
        max_length=128,
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

    def check_password(self, password):
        return not self.password_hash or check_password(password, self.password_hash)

    @property
    def websocket_url(self):
        return f'{WEBSOCKETS_URL}/{self.code}'

    def __str__(self):
        return f'ChargePoint (id={self.id}, status={self.status}, location={self.location})'


class Transaction(models.Model):
    class Meta:
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')

    transaction_id = models.AutoField(
        primary_key=True
    )

    city = models.CharField(
        max_length=48
    )

    vehicle = models.CharField(
        max_length=48
    )

    address = models.CharField(
        max_length=100
    )

    meter_start = models.IntegerField()

    meter_stop = models.IntegerField(
        null=True,
        blank=True,
    )

    charge_point = models.ForeignKey(
        ChargePoint,
        on_delete=models.CASCADE,
        related_name='transactions',
    )
