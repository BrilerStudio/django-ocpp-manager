from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ChargePointNodeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'charge_point_node'

    verbose_name = _('OCPP Charge Point Node')
