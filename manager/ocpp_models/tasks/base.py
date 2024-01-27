from ocpp.v16.enums import Action
from pydantic import BaseModel

from app.fields import ConnectionStatus
from app.settings import TASKS_EXCHANGE_NAME, REGULAR_MESSAGE_PRIORITY


class BaseTask(BaseModel):
    message_id: str
    charge_point_id: str
    action: ConnectionStatus | Action
    exchange: str = TASKS_EXCHANGE_NAME
    priority: int = REGULAR_MESSAGE_PRIORITY
