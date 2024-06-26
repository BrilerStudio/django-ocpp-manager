from manager.ocpp_events.base import BaseEvent
from app.fields import ConnectionStatus


class OnConnectionEvent(BaseEvent):
    action: ConnectionStatus = ConnectionStatus.NEW_CONNECTION


class LostConnectionEvent(BaseEvent):
    action: ConnectionStatus = ConnectionStatus.LOST_CONNECTION
