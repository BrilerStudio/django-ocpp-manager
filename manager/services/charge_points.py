from django.db.models import Count

from manager.models import ChargePoint
from manager.ocpp_events.status_notification import StatusNotificationEvent
from manager.views.charge_points import ConnectorView


async def update_connectors(event: StatusNotificationEvent):
    charge_point = await ChargePoint.objects.aget(charge_point_id=event.charge_point_id)
    connector_data = ConnectorView(status=event.payload.status).model_dump_json()
    if event.payload.connector_id == 1:
        charge_point.connectors = {event.payload.connector_id: connector_data}
    else:
        charge_point.connectors.update({event.payload.connector_id: connector_data})
    await charge_point.save()


async def get_statuses_counts(account_id):
    # TODO: refactor this
    result = await ChargePoint.objects.filter(location__account_id=account_id).values('status').annotate(
        count=Count('status')
    )

    return {item['status'].lower(): item['count'] for item in result}
