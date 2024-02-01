from ocpp.v16.enums import AuthorizationStatus

from manager.models import ChargePoint, Transaction, TransactionStatus
from manager.ocpp_events.authorize import AuthorizeEvent
from manager.ocpp_models.tasks.authorize import AuthorizeTask
from utils.logging import logger


async def process_authorize(event: AuthorizeEvent) -> AuthorizeTask:
    logger.info(f'Start process Authorize (event={event})')
    charge_point = await ChargePoint.objects.aget(charge_point_id=event.charge_point_id)

    try:
        transaction = await Transaction.objects.aget(
            charge_point=charge_point,
            tag_id=event.payload.id_tag,
            status=TransactionStatus.initialized.value,
            meter_start__isnull=True,
        )
    except Transaction.DoesNotExist:
        logger.info(
            f'Reject authorize '
            f'(charge_point_id={event.charge_point_id}, '
            f'message_id={event.message_id},'
            f'payload={event.payload}).'
        )
        return AuthorizeTask(
            message_id=event.message_id,
            charge_point_id=event.charge_point_id,
            id_tag_info={'status': AuthorizationStatus.invalid.value},
        )

    return AuthorizeTask(
        message_id=event.message_id,
        charge_point_id=event.charge_point_id,
        id_tag_info={'status': AuthorizationStatus.accepted.value},
    )
