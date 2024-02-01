import asyncio

from app.celery import LoggingTask, app
from manager.models import Transaction
from manager.services.ocpp.remote_start_transaction import remote_start_transaction
from manager.services.ocpp.remote_stop_transaction import remote_stop_transaction
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

    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(remote_start_transaction(transaction))


@app.task(
    base=LoggingTask,
    bind=True,
    retry_kwargs={'max_retries': 5},
    autoretry_for=(Exception,),
    default_retry_delay=2
)
def remote_stop_transaction_task(
        task, transaction_id: int,
):
    transaction = Transaction.objects.select_related('charge_point').get(transaction_id=transaction_id)
    logger.info(f'Got transaction (transaction={transaction}).')

    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(remote_stop_transaction(transaction))
