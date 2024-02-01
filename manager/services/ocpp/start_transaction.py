from ocpp.v16.enums import AuthorizationStatus

from manager.models import Transaction, ChargePoint, TransactionStatus
from manager.ocpp_events.start_transaction import StartTransactionEvent
from manager.ocpp_models.tasks.start_transaction import StartTransactionTask
from utils.logging import logger


async def process_start_transaction(
        event: StartTransactionEvent,
) -> StartTransactionTask:
    logger.info(f'Start process StartTransaction (event={event})')
    charge_point = await ChargePoint.objects.aget(charge_point_id=event.charge_point_id)

    try:
        transaction = await Transaction.objects.aget(
            connector_id=event.payload.connector_id,
            charge_point=charge_point,
            tag_id=event.payload.id_tag,
            status=TransactionStatus.initialized.value,
            meter_start__isnull=True,
        )
    except Transaction.DoesNotExist:
        logger.info(
            f'Reject transaction '
            f'(charge_point_id={event.charge_point_id}, '
            f'message_id={event.message_id},'
            f'payload={event.payload}).',
        )
        return StartTransactionTask(
            message_id=event.message_id,
            charge_point_id=event.charge_point_id,
            transaction_id=event.transaction_id,
            id_tag_info={'status': AuthorizationStatus.invalid.value},
        )
    update_fields = []
    if not transaction.vehicle:
        update_fields.append('vehicle')
        transaction.vehicle = event.payload.id_tag

    transaction.meter_start = event.payload.meter_start
    transaction.status = TransactionStatus.started.value
    transaction.connector_id = event.payload.connector_id
    update_fields += ['meter_start', 'status', 'connector_id']
    await transaction.asave(
        update_fields=update_fields,
    )

    return StartTransactionTask(
        message_id=event.message_id,
        charge_point_id=event.charge_point_id,
        transaction_id=transaction.transaction_id,
        id_tag_info={'status': AuthorizationStatus.accepted.value},
    )
