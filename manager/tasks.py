import asyncio

from app.celery import LoggingTask, app
from manager.models import Transaction
from manager.services.ocpp.remote_start_transaction import remote_start_transaction
from utils.logging import logger


@app.task(
    base=LoggingTask,
    bind=True
)
def remote_start_transaction_task(
        task, transaction_id: int,
):
    transaction = Transaction.objects.select_related('charge_point').get(transaction_id=transaction_id)
    logger.info(f'Got transaction (transaction={transaction}).')

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(remote_start_transaction(transaction))
    loop.close()
