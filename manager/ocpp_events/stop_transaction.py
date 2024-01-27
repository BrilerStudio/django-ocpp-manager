from ocpp.v16.enums import Action

from manager.ocpp_events.base import BaseEvent
from ocpp.v16.call import StopTransactionPayload


class StopTransactionEvent(BaseEvent):
    action: Action = Action.StopTransaction
    payload: StopTransactionPayload
    transaction_id: int | None = None
