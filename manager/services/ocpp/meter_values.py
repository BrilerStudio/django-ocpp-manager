from manager.ocpp_models.tasks.meter_values import MeterValuesTask
from manager.ocpp_events.meter_values import MeterValuesEvent


async def process_meter_values(
        event: MeterValuesEvent
) -> MeterValuesTask:

    payload = event.payload

    return MeterValuesTask(
        message_id=event.message_id,
        charge_point_id=event.charge_point_id
    )
