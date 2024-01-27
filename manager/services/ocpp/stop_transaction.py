from ocpp.v16.enums import AuthorizationStatus

from manager.models import Transaction
from manager.ocpp_events.stop_transaction import StopTransactionEvent
from manager.ocpp_models.tasks.stop_transaction import StopTransactionTask


async def process_stop_transaction(
        event: StopTransactionEvent,
) -> StopTransactionTask:
    await Transaction.objects.filter(transaction_id=event.payload.transaction_id).aupdate(
        meter_stop=event.payload.meter_stop,
    )

    return StopTransactionTask(
        message_id=event.message_id,
        charge_point_id=event.charge_point_id,
        id_tag_info={'status': AuthorizationStatus.accepted.value},
    )
