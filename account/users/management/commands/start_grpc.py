import asyncio
from typing import Any

from django.core.management.base import BaseCommand

from users.tasks_server import tasks_serve


class Command(BaseCommand):  # type: ignore
    help = "start grpc server"

    def handle(self, *args: Any, **options: Any) -> None:
        asyncio.run(tasks_serve())
