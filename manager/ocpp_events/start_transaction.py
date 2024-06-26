from ocpp.v16.enums import Action

from manager.ocpp_events.base import BaseEvent
from ocpp.v16.call import StartTransactionPayload


class StartTransactionEvent(BaseEvent):
    action: Action = Action.StartTransaction
    payload: StartTransactionPayload
    transaction_id: int | str | None = None
