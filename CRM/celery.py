from __future__ import absolute_import, unicode_literals
import os

import CRM.tasks

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CRM.settings')

app = Celery('CRM')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.timezone = 'Europe/Kyiv'

app.conf.update(
    broker_url='redis://localhost:6379/0',
    broker_connection_retry_on_startup=True,
)

app.autodiscover_tasks()


app.conf.beat_schedule = {
    # 'daily_get_sup_products': {
    #     'task': 'product.tasks.fetch_suppliers_data',
    #     'schedule': crontab(minute=0) # , hour='*/1'
    # },
    'load_orders_ttn_data': {
        'task': 'order.tasks.get_ttns_status',
        'schedule': crontab(minute=0)
    },
    "daily_backup": {
        "task": "tasks.backup_db",
        "schedule": crontab(hour=0, minute=0),
    },
}