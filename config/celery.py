import os
from celery import Celery

# Windows에서 fork 방식 설정
if os.name == 'nt':
    import multiprocessing
    multiprocessing.set_start_method('spawn', force=True)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()