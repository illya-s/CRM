from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CRM.settings')

app = Celery('CRM')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'get_sup_products_every_hour_minutes': {
        'task': 'product.tasks.fetch_suppliers_data',
        'schedule': crontab(minute=0) # , hour='*/1'
    },
    'load_orders_ttn_data': {
        'task': 'order.tasks.fetch_orders_data',
        'schedule': crontab(minute=0)
    }
}