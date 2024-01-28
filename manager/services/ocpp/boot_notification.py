from ocpp.v16.enums import RegistrationStatus, ChargePointStatus

from app.utils import get_utc_as_string
from manager.models import ChargePoint
from manager.ocpp_events.boot_notification import BootNotificationEvent
from manager.ocpp_models.tasks.boot_notification import BootNotificationTask
from utils.logging import logger


async def process_boot_notification(
        event: BootNotificationEvent
) -> BootNotificationTask:
    logger.info(f'Start process BootNotification (event={event})')

    data = {
        'model': event.payload.charge_point_model,
        'serial_number': event.payload.charge_point_serial_number,
        'manufacturer': event.payload.charge_point_vendor,
    }
    data = {k: v for k, v in data.items() if v}

    await ChargePoint.objects.filter(charge_point_id=event.charge_point_id).aupdate(
        status=ChargePointStatus.available,
        **data,
    )

    return BootNotificationTask(
        message_id=event.message_id,
        charge_point_id=event.charge_point_id,
        current_time=get_utc_as_string(),
        interval=20,
        status=RegistrationStatus.accepted
    )
