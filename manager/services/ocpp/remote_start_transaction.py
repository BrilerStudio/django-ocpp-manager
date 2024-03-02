import uuid

from app.queue.publisher import publish
from app.settings import REGULAR_MESSAGE_PRIORITY
from manager.audit_logs import audit_log
from manager.models import Transaction, TransactionStatus
from manager.ocpp_models.tasks.remote_start_transaction import RemoteStartTransactionTask
from utils.logging import logger


async def remote_start_transaction(
        transaction: Transaction,
):
    logger.info(f'Remote start transaction (transaction={transaction})')

    await Transaction.objects.filter(
        transaction_id=transaction.transaction_id,
        status=TransactionStatus.initialized.value,
    ).aupdate(
        status=TransactionStatus.requested.value,
    )

    task = RemoteStartTransactionTask(
        charge_point_id=transaction.charge_point.charge_point_id,
        id_tag=transaction.tag_id,
        connector_id=transaction.connector_id,
        message_id=str(uuid.uuid4()),
        priority=REGULAR_MESSAGE_PRIORITY,
    )

    await publish(task.model_dump_json(), to=task.exchange, priority=task.priority)
    await audit_log(
        charge_point=transaction.charge_point,
        action=task.action,
        action_type='sent',
        data=task.model_dump(),
    )
