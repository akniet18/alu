import os 
from celery import Celery 
# Set default Django settings 
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alu.settings') 
app = Celery('alu')   
app.config_from_object('django.conf:settings', namespace='CELERY')   
app.autodiscover_tasks()

# app.conf.beat_schedule = {
#     'send_notifiction_every_day': {
#         'task': 'basket.tasks.send_notifiction',
#         'schedule': 10,  # change to `crontab(minute=0, hour=0)` if you want it to run daily at midnight
#     },
# }