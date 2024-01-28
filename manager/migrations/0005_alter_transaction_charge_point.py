# Generated by Django 5.0.1 on 2024-01-28 11:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("manager", "0004_alter_chargepoint_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="charge_point",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="transactions",
                to="manager.chargepoint",
            ),
        ),
    ]
