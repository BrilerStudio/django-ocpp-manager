from __future__ import annotations

from functools import wraps
from typing import Callable, Union

from loguru import logger
from ocpp.v16.enums import Action
from websockets.legacy.server import WebSocketServer

from charge_point_node.router import Router
from app.fields import ConnectionStatus
from manager.ocpp_models.tasks.boot_notification import BootNotificationTask
from manager.ocpp_models.tasks.heartbeat import HeartbeatTask
from manager.ocpp_models.tasks.status_notification import StatusNotificationTask
from manager.ocpp_models.tasks.security_event_notification import SecurityEventNotificationTask
from manager.ocpp_models.tasks.authorize import AuthorizeTask
from manager.ocpp_models.tasks.start_transaction import StartTransactionTask
from manager.ocpp_models.tasks.stop_transaction import StopTransactionTask
from manager.ocpp_models.tasks.meter_values import MeterValuesTask

router = Router()


def prepare_task(func) -> Callable:
    @wraps(func)
    async def wrapper(data, *args, **kwargs):
        task = {
            Action.StatusNotification: StatusNotificationTask,
            Action.BootNotification: BootNotificationTask,
            Action.Heartbeat: HeartbeatTask,
            Action.SecurityEventNotification: SecurityEventNotificationTask,
            Action.Authorize: AuthorizeTask,
            Action.StartTransaction: StartTransactionTask,
            Action.StopTransaction: StopTransactionTask,
            Action.MeterValues: MeterValuesTask
        }[data["action"]](**data)
        return await func(task, *args, **kwargs)

    return wrapper


@prepare_task
async def process_task(
        task: Union[
            StatusNotificationTask,
            BootNotificationTask,
            HeartbeatTask,
            SecurityEventNotificationTask,
            AuthorizeTask,
            StartTransactionTask,
            StopTransactionTask,
            MeterValuesTask
        ],
        server: WebSocketServer
) -> None:
    logger.info(f"Got task from manager (task={task})")
    connections = [conn for conn in server.websockets if conn.charge_point_id == task.charge_point_id]
    if not connections:
        return
    connection = connections[0]

    if task.action is ConnectionStatus.DISCONNECT:
        await connection.close()
        return

    await router.handle_out(connection, task)
