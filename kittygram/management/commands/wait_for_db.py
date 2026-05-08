import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Команда для ожидания готовности базы данных"""

    def handle(self, *args, **options):
        self.stdout.write('Ожидание подключения к базе данных...')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default'].cursor()
            except OperationalError:
                self.stdout.write('База данных недоступна, ждём 1 секунду...')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('База данных готова!'))