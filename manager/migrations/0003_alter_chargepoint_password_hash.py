# Generated by Django 5.0.1 on 2024-01-28 11:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("manager", "0002_alter_chargepoint_options_alter_location_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="chargepoint",
            name="password_hash",
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
