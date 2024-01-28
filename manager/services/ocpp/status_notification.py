from ocpp.v16.enums import ChargePointStatus

from manager.models import ChargePoint
from manager.ocpp_events.status_notification import StatusNotificationEvent
from manager.ocpp_models.tasks.status_notification import StatusNotificationTask
from manager.services.charge_points import update_connectors


async def process_status_notification(
        event: StatusNotificationEvent
) -> StatusNotificationTask:

    await update_connectors(event)

    if event.payload.connector_id == 0:
        await ChargePoint.objects.filter(charge_point_id=event.charge_point_id).aupdate(
            status=ChargePointStatus.available,
        )

    return StatusNotificationTask(
        message_id=event.message_id,
        charge_point_id=event.charge_point_id
    )
