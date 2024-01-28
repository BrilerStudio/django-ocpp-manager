import asyncio

from django.core.management.base import BaseCommand

from app.queue.consumer import start_consume
from app.settings import EVENTS_EXCHANGE_NAME
from manager.events import process_event


class Command(BaseCommand):
    help = 'Start OCPP consumer'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        asyncio.run(start_consume(exchange_name=EVENTS_EXCHANGE_NAME, on_message=process_event))
