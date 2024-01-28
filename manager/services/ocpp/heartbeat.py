from ocpp.v16.enums import ChargePointStatus

from app.utils import get_utc_as_string
from manager.models import ChargePoint
from manager.ocpp_events.heartbeat import HeartbeatEvent
from manager.ocpp_models.tasks.heartbeat import HeartbeatTask


async def process_heartbeat(event: HeartbeatEvent) -> HeartbeatTask:
    # Do some logic here
    await ChargePoint.objects.filter(charge_point_id=event.charge_point_id).aupdate(
        status=ChargePointStatus.available,
    )

    return HeartbeatTask(
        message_id=event.message_id,
        charge_point_id=event.charge_point_id,
        current_time=get_utc_as_string()
    )
