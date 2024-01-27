from ocpp.v16.enums import Action, RegistrationStatus

from manager.ocpp_models.tasks.base import BaseTask


class StatusNotificationTask(BaseTask):
    action: Action = Action.StatusNotification
