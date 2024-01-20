from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_service.settings')

app = Celery('shop_service')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check_expired_sales': {
        'task': 'product_app.tasks.delete_expired_objects',
        'schedule': 60,
    },
}
