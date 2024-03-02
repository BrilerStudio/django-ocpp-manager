from typing import Dict

from ocpp.v16.enums import Action, RegistrationStatus

from manager.ocpp_models.tasks.base import BaseTask


class StartTransactionTask(BaseTask):
    action: Action = Action.StartTransaction
    transaction_id: int = None
    id_tag_info: Dict
