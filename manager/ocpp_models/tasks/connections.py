from app.fields import ConnectionStatus
from manager.ocpp_models.tasks.base import BaseTask


class DisconnectTask(BaseTask):
    charge_point_id: str
    name: ConnectionStatus = ConnectionStatus.DISCONNECT
