import uuid

from app.queue.publisher import publish
from app.settings import REGULAR_MESSAGE_PRIORITY
from manager.audit_logs import audit_log
from manager.models import Transaction, TransactionStatus
from manager.ocpp_models.tasks.remote_stop_transaction import RemoteStopTransactionTask
from utils.logging import logger


async def remote_stop_transaction(
        transaction: Transaction,
):
    logger.info(f'Remote stop transaction (transaction={transaction})')

    await Transaction.objects.filter(
        transaction_id=transaction.transaction_id,
        status=TransactionStatus.started.value,
    ).aupdate(
        status=TransactionStatus.stopping.value,
    )

    task = RemoteStopTransactionTask(
        charge_point_id=transaction.charge_point.charge_point_id,
        transaction_id=transaction.transaction_id,
        message_id=str(uuid.uuid4()),
        priority=REGULAR_MESSAGE_PRIORITY,
    )

    await publish(task.model_dump_json(), to=task.exchange, priority=task.priority)
    await audit_log(
        charge_point=transaction.charge_point,
        action=f'Send request {task.action} {task.message_id or ""}'.strip(),
        data=task.model_dump(),
    )
