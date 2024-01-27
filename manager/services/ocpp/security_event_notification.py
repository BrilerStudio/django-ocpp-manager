from manager.ocpp_models.tasks.security_event_notification import SecurityEventNotificationTask
from manager.ocpp_events.security_event_notification import SecurityEventNotificationEvent


async def process_security_event_notification(
        event: SecurityEventNotificationEvent
) -> SecurityEventNotificationTask:
    # Do some logic here

    return SecurityEventNotificationTask(
        message_id=event.message_id,
        charge_point_id=event.charge_point_id
    )
