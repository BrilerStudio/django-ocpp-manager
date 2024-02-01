from ocpp.v16.enums import Action

from manager.ocpp_models.tasks.base import BaseTask


class RemoteStopTransactionTask(BaseTask):
    action: Action = Action.RemoteStopTransaction
    transaction_id: int
