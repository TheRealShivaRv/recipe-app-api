import time
from django.db import connections
# from django.db import ConnectionDoesNotExist
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        self.stdout.write('Waiting for the Database...')
        db_conn = None
        while db_conn == None:
            try:
                db_conn = connections['default']
            except OperationalError:
                waitTime = 1
                output = "Couldn't connect to the database, waiting for " + \
                    str(waitTime) + " second"
                self.stdout.write(output)
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS(
            'Database successfully connected'))
