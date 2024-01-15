import os

from celery.app import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_service.settings')
app = Celery('shop_service')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.broker_url = settings.CELERY_BROKER_URL

app.autodiscover_tasks()
