import traceback
from copy import deepcopy
from functools import wraps
from typing import Callable, Union

from django.utils import timezone
from ocpp.v16.enums import Action, ChargePointStatus

from app.fields import ConnectionStatus
from app.queue.publisher import publish
from manager.audit_logs import audit_log
from manager.models import ChargePoint
from manager.ocpp_events.authorize import AuthorizeEvent
from manager.ocpp_events.base import BaseEvent
from manager.ocpp_events.boot_notification import BootNotificationEvent
from manager.ocpp_events.heartbeat import HeartbeatEvent
from manager.ocpp_events.meter_values import MeterValuesEvent
from manager.ocpp_events.on_connection import LostConnectionEvent
from manager.ocpp_events.security_event_notification import (
    SecurityEventNotificationEvent,
)
from manager.ocpp_events.start_transaction import StartTransactionEvent
from manager.ocpp_events.status_notification import StatusNotificationEvent
from manager.ocpp_events.stop_transaction import StopTransactionEvent
from manager.services.ocpp.authorize import process_authorize
from manager.services.ocpp.boot_notification import process_boot_notification
from manager.services.ocpp.heartbeat import process_heartbeat
from manager.services.ocpp.meter_values import process_meter_values
from manager.services.ocpp.security_event_notification import (
    process_security_event_notification,
)
from manager.services.ocpp.start_transaction import process_start_transaction
from manager.services.ocpp.status_notification import process_status_notification
from manager.services.ocpp.stop_transaction import process_stop_transaction
from utils.logging import logger


def prepare_event(func) -> Callable:
    @wraps(func)
    async def wrapper(data):
        logger.info(f'Got event from charge point node (event={data})')

        event = {
            ConnectionStatus.LOST_CONNECTION: LostConnectionEvent,
            Action.StatusNotification: StatusNotificationEvent,
            Action.BootNotification: BootNotificationEvent,
            Action.Heartbeat: HeartbeatEvent,
            Action.SecurityEventNotification: SecurityEventNotificationEvent,
            Action.Authorize: AuthorizeEvent,
            Action.StartTransaction: StartTransactionEvent,
            Action.StopTransaction: StopTransactionEvent,
            Action.MeterValues: MeterValuesEvent,
        }[data['action']](**data)
        return await func(event)

    return wrapper


@prepare_event
async def process_event(
        event: Union[
            LostConnectionEvent,
            StatusNotificationEvent,
            BootNotificationEvent,
            HeartbeatEvent,
            SecurityEventNotificationEvent,
            AuthorizeEvent,
            StartTransactionEvent,
            StopTransactionEvent,
            MeterValuesEvent,
        ],
) -> BaseEvent | None:
    charge_point = await ChargePoint.objects.aget(charge_point_id=event.charge_point_id)
    charge_point.last_seen_at = timezone.now()
    await charge_point.asave()

    await audit_log(
        charge_point=charge_point,
        action=f'Received {event.action} {event.message_id or ""}'.strip(),
        data=event.model_dump(),
    )

    try:
        task = None

        if event.action is Action.MeterValues:
            task = await process_meter_values(deepcopy(event))
        if event.action is Action.StopTransaction:
            task = await process_stop_transaction(deepcopy(event))
            event.transaction_id = event.payload.transaction_id
        if event.action is Action.StartTransaction:
            task = await process_start_transaction(deepcopy(event))
            event.transaction_id = task.transaction_id
        if event.action is Action.Authorize:
            task = await process_authorize(deepcopy(event))
        if event.action is Action.SecurityEventNotification:
            task = await process_security_event_notification(deepcopy(event))
        if event.action is Action.BootNotification:
            task = await process_boot_notification(deepcopy(event))
        if event.action is Action.StatusNotification:
            task = await process_status_notification(deepcopy(event))
        if event.action is Action.Heartbeat:
            task = await process_heartbeat(deepcopy(event))

        if event.action is ConnectionStatus.LOST_CONNECTION:
            await ChargePoint.objects.filter(charge_point_id=event.charge_point_id).aupdate(
                status=ChargePointStatus.unavailable,
            )

        if task:
            await publish(task.model_dump_json(), to=task.exchange, priority=task.priority)
            await audit_log(
                charge_point=charge_point,
                action=f'Sent response {task.action} {event.message_id or ""}'.strip(),
                data=task.model_dump(),
            )

        logger.info(f'Successfully completed process event={event}')

        return event
    except Exception as e:
        logger.exception(e)
        full_trace = traceback.format_exc()
        await audit_log(
            charge_point=charge_point,
            action=f'Error during process event {event.action} {event.message_id or ""}'.strip(),
            data=full_trace,
        )
