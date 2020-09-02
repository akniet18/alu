from celery import task 
from celery import shared_task 
from celery.task.schedules import crontab
from celery.task import periodic_task
from datetime import timedelta
# We can have either registered task 
# @task(name='summary') 
# def send_import_summary():
#     # Magic happens here ... 
# # or 
@shared_task
def send_notifiction():
    print('Here I\’m')
     # Another trick