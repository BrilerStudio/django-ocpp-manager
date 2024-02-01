import asyncio

from django.core.management.base import BaseCommand

from manager.transactions_manager import run_transactions_manager


class Command(BaseCommand):
    help = 'Start OCPP transactions manager'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        asyncio.run(run_transactions_manager())
