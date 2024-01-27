# Generated by Django 5.0.1 on 2024-01-27 15:24

import django.db.models.deletion
import ocpp.v16.enums
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=48, unique=True)),
                ('city', models.CharField(max_length=48)),
                ('address1', models.CharField(max_length=48)),
                ('address2', models.CharField(blank=True, max_length=100, null=True)),
                ('comment', models.TextField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('city', models.CharField(max_length=48)),
                ('vehicle', models.CharField(max_length=48)),
                ('address', models.CharField(max_length=100)),
                ('meter_start', models.IntegerField()),
                ('meter_stop', models.IntegerField(blank=True, null=True)),
                ('charge_point', models.CharField(max_length=48)),
                ('transaction_id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='ChargePoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=48, null=True)),
                (
                    'status',
                    models.CharField(
                        choices=[
                            (ocpp.v16.enums.ChargePointStatus['available'], 'Available'),
                            (ocpp.v16.enums.ChargePointStatus['preparing'], 'Preparing'),
                            (ocpp.v16.enums.ChargePointStatus['charging'], 'Charging'),
                            (ocpp.v16.enums.ChargePointStatus['suspended_evse'], 'SuspendedEVSE'),
                            (ocpp.v16.enums.ChargePointStatus['suspended_ev'], 'SuspendedEV'),
                            (ocpp.v16.enums.ChargePointStatus['finishing'], 'Finishing'),
                            (ocpp.v16.enums.ChargePointStatus['reserved'], 'Reserved'),
                            (ocpp.v16.enums.ChargePointStatus['unavailable'], 'Unavailable'),
                            (ocpp.v16.enums.ChargePointStatus['faulted'], 'Faulted'),
                        ],
                        default=ocpp.v16.enums.ChargePointStatus['unavailable'],
                        max_length=50,
                    ),
                ),
                ('manufacturer', models.CharField(max_length=48)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('serial_number', models.CharField(max_length=48, unique=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('model', models.CharField(max_length=48)),
                ('password', models.CharField(blank=True, max_length=48, null=True)),
                ('connectors', models.JSONField(default=dict)),
                (
                    'location',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='charge_points',
                        to='manager.location',
                    ),
                ),
            ],
        ),
    ]