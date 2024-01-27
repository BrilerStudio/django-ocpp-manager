import asyncio

from app.queue.consumer import start_consume
from app.settings import EVENTS_EXCHANGE_NAME
from manager.events import process_event


async def on_startup():
    task = asyncio.create_task(
        start_consume(exchange_name=EVENTS_EXCHANGE_NAME, on_message=process_event),
    )
