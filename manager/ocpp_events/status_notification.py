from ocpp.v16.enums import Action
from ocpp.v16.call import StatusNotificationPayload

from manager.ocpp_events.base import BaseEvent


class StatusNotificationEvent(BaseEvent):
    action: Action = Action.StatusNotification
    payload: StatusNotificationPayload
