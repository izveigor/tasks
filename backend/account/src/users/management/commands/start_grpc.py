import asyncio
from typing import Any

from django.core.management.base import BaseCommand

from account.users_server import users_serve


class Command(BaseCommand):  # type: ignore
    help = "start grpc server"

    def handle(self, *args: Any, **options: Any) -> None:
        asyncio.run(users_serve())  # type: ignore
