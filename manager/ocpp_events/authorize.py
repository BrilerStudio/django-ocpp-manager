from ocpp.v16.enums import Action
from ocpp.v16.call import AuthorizePayload

from manager.ocpp_events.base import BaseEvent


class AuthorizeEvent(BaseEvent):
    action: Action = Action.Authorize
    payload: AuthorizePayload
