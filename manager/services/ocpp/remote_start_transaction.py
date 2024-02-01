import uuid

from manager.models import Transaction, TransactionStatus
from manager.ocpp_models.tasks.remote_start_transaction import RemoteStartTransactionTask
from utils.logging import logger


async def remote_start_transaction(
        transaction: Transaction,
) -> RemoteStartTransactionTask:
    logger.info(f'Remote start transaction (transaction={transaction})')

    await Transaction.objects.filter(
        transaction_id=transaction.transaction_id,
        status=TransactionStatus.initialized.value,
    ).aupdate(
        status=TransactionStatus.requested.value,
    )

    return RemoteStartTransactionTask(
        charge_point_id=transaction.charge_point.charge_point_id,
        id_tag=transaction.tag_id,
        connector_id=transaction.connector_id,
        message_id=str(uuid.uuid4()),
    )
