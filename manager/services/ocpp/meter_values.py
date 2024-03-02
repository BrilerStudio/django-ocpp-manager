from manager.models import Transaction
from manager.ocpp_events.meter_values import MeterValuesEvent
from manager.ocpp_models.tasks.meter_values import MeterValuesTask
from utils.logging import logger


async def process_meter_values(
        event: MeterValuesEvent
) -> MeterValuesTask:
    logger.info(f'Start process MeterValues (event={event}), payload={event.payload})')

    try:
        transaction = await Transaction.objects.aget(transaction_id=event.payload.transaction_id)
        transaction.meter_value_raw = event.payload.meter_value
        await transaction.asave()
    except Transaction.DoesNotExist:
        logger.error(
            f'Got meter value for unknown transaction '
            f'(charge_point_id={event.charge_point_id}, '
            f'message_id={event.message_id},'
            f'payload={event.payload}).',
        )
        raise Exception('Got meter value for unknown transaction')

    return MeterValuesTask(
        message_id=event.message_id,
        charge_point_id=event.charge_point_id
    )
