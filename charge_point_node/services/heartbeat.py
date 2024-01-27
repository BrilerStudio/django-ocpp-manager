from ocpp.v16.call_result import HeartbeatPayload as CallResultHeartbeatPayload
from ocpp.v16.enums import Action

from app.queue.publisher import publish
from charge_point_node.models.heartbeat import HeartbeatEvent
from charge_point_node.router import Router
from manager.ocpp_models.tasks.heartbeat import HeartbeatTask
from utils.logging import logger

router = Router()


@router.on(Action.Heartbeat)
async def on_heartbeat(
    message_id: str,
    charge_point_id: str,
    **kwargs,
):
    logger.info(
        f'Start accept heartbeat '
        f'(charge_point_id={charge_point_id}, '
        f'message_id={message_id},'
        f'payload={kwargs}).',
    )
    event = HeartbeatEvent(
        charge_point_id=charge_point_id,
        message_id=message_id,
    )
    await publish(event.json(), to=event.exchange, priority=event.priority)


@router.out(Action.Heartbeat)
async def respond_heartbeat(task: HeartbeatTask) -> CallResultHeartbeatPayload:
    logger.info(f'Start respond heartbeat task={task}).')
    return CallResultHeartbeatPayload(current_time=task.current_time)
