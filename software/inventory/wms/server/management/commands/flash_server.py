from django.core.management.base import BaseCommand
import subprocess

class Command(BaseCommand):
    help = 'Starts the Django server and Celery worker and beat'

    def handle(self, *args, **options):
        server_process = subprocess.Popen(['py', 'manage.py', 'runserver'])
        worker_process = subprocess.Popen(['celery', '-A', 'wms', 'worker', '-l', 'info', '-P', 'eventlet'])
        beat_process = subprocess.Popen(['celery', '-A', 'wms', 'beat', '-l', 'info'])
        try:
            server_process.wait()
        except KeyboardInterrupt:
            server_process.terminate()
            worker_process.terminate()
            beat_process.terminate()