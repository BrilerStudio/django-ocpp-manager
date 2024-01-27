from ocpp.v16.enums import Action

from manager.ocpp_events.base import BaseEvent


class HeartbeatEvent(BaseEvent):
    action: Action = Action.Heartbeat
