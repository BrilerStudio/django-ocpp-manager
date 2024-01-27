from ocpp.v16.enums import Action
from ocpp.v16.call import BootNotificationPayload

from manager.ocpp_events.base import BaseEvent


class BootNotificationEvent(BaseEvent):
    action: Action = Action.BootNotification
    payload: BootNotificationPayload
