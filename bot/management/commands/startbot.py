import asyncio
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Starts the telegram bots'

    def handle(self, *args, **options):
        from bot.initializer import main
        asyncio.run(main())
