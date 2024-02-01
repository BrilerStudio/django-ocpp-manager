from ocpp.v16.enums import AuthorizationStatus

from manager.models import Transaction, TransactionStatus
from manager.ocpp_events.stop_transaction import StopTransactionEvent
from manager.ocpp_models.tasks.stop_transaction import StopTransactionTask
from utils.logging import logger


async def process_stop_transaction(
        event: StopTransactionEvent,
) -> StopTransactionTask:
    logger.info(
        f'Start process StopTransaction (event={event})'
        f'payload={event.payload})'
    )

    await Transaction.objects.filter(transaction_id=event.payload.transaction_id, tag_id=event.payload.id_tag).aupdate(
        meter_stop=event.payload.meter_stop,
        status=TransactionStatus.started.value
    )

    return StopTransactionTask(
        message_id=event.message_id,
        charge_point_id=event.charge_point_id,
        id_tag_info={'status': AuthorizationStatus.accepted.value},
    )
