from ocpp.v16.enums import AuthorizationStatus

from manager.ocpp_events.authorize import AuthorizeEvent
from manager.ocpp_models.tasks.authorize import AuthorizeTask


async def process_authorize(event: AuthorizeEvent) -> AuthorizeTask:
    return AuthorizeTask(
        message_id=event.message_id,
        charge_point_id=event.charge_point_id,
        id_tag_info={'status': AuthorizationStatus.accepted.value},
    )
