import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_service.settings')
app = Celery('shop_service')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
