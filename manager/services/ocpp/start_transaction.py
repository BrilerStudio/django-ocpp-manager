from ocpp.v16.enums import AuthorizationStatus

from manager.models import Transaction, ChargePoint
from manager.ocpp_events.start_transaction import StartTransactionEvent
from manager.ocpp_models.tasks.start_transaction import StartTransactionTask
from utils.logging import logger


async def process_start_transaction(
        event: StartTransactionEvent,
) -> StartTransactionTask:
    logger.info(f'Start process StartTransaction (event={event})')
    charge_point = await ChargePoint.objects.aget(event.charge_point_id)

    transaction = await Transaction.objects.acreate(
        city=charge_point.location.city,
        address=charge_point.location.address1,
        vehicle=event.payload.id_tag,
        meter_start=event.payload.meter_start,
        charge_point=charge_point.id,
        account_id=charge_point.location.account.id,
    )

    return StartTransactionTask(
        message_id=event.message_id,
        charge_point_id=event.charge_point_id,
        transaction_id=transaction.transaction_id,
        id_tag_info={'status': AuthorizationStatus.accepted.value},
    )
