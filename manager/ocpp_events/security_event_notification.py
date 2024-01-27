from ocpp.v16.enums import Action

from manager.ocpp_events.base import BaseEvent


class SecurityEventNotificationEvent(BaseEvent):
    action: Action = Action.SecurityEventNotification
