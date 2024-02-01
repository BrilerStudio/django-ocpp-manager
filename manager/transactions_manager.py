import asyncio

from app.queue.publisher import publish
from manager.models import Transaction, TransactionStatus
from manager.services.ocpp.remote_start_transaction import remote_start_transaction
from utils.logging import logger


async def process_start_transaction(transaction: Transaction):
    task = await remote_start_transaction(transaction)

    if task:
        await publish(task.model_dump_json(), to=task.exchange, priority=task.priority)


async def run_transactions_manager():
    while True:
        logger.info('Start process transactions')
        async for transaction in Transaction.objects.filter(status=TransactionStatus.initialized.value).select_related(
                'charge_point',
        ):
            await process_start_transaction(transaction)

        logger.info('Finish process transactions, sleep 3 seconds')
        await asyncio.sleep(3)
