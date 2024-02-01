from ocpp.v16.enums import ChargePointStatus

from manager.models import ChargePoint
from manager.ocpp_events.status_notification import StatusNotificationEvent
from manager.ocpp_models.tasks.status_notification import StatusNotificationTask


async def process_status_notification(
        event: StatusNotificationEvent
) -> StatusNotificationTask:

    charge_point = await ChargePoint.objects.aget(charge_point_id=event.charge_point_id)
    charge_point.status = event.payload.status
    connector_data = {
        'status': event.payload.status
    }
    charge_point.connectors[event.payload.connector_id] = connector_data
    await charge_point.asave()

    if event.payload.connector_id == 0:
        await ChargePoint.objects.filter(charge_point_id=event.charge_point_id).aupdate(
            status=ChargePointStatus.available,
        )

    return StatusNotificationTask(
        message_id=event.message_id,
        charge_point_id=event.charge_point_id
    )
