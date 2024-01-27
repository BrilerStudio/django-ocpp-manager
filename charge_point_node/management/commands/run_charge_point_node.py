import asyncio

from django.core.management.base import BaseCommand

from charge_point_node.main import main


class Command(BaseCommand):
    help = 'Start charge point node'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        asyncio.run(main())
