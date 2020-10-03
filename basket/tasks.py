# from celery import shared_task, task
# from celery.task.schedules import crontab
# from celery.task import periodic_task
from products.views import send_push
from datetime import datetime, timedelta
# from django.apps import apps
# from celery import app
from products.models import Product
from message.models import Message
from utils.messages import deliverThree, PickupThree
from huey import crontab
from utils.push import send_push
from huey.contrib.djhuey import db_periodic_task, db_task

# @periodic_task(run_every=timedelta(seconds=10))
@db_periodic_task(crontab(minute=0, hour=9))
def send_notifiction():    
    p = Product.objects.filter(is_rented=True, count_day__isnull=False, rented_obj__is_rented=True)
    for i in p:
        r = i.rented_obj.all()[0]
        rented = datetime.strptime(str(r.rented_day), '%Y-%m-%d')
        deadline = rented + timedelta(i.count_day)
        days_left = datetime.now()-deadline
        days_left = int(days_left.total_seconds()) // (24 * 3600)
        print(days_left)
        if days_left == -1:            
            if r.return_product == 1:
                mid = Message.objects.create(
                    user = r.user,
                    text = deliverThree(i.title),
                    action = 2,
                    order = r,
                    product = i,
                    get_or_return = 2,
                    ownerorclient = 2,
                    words = [i.title]
                )
                send_push(r.user, mid.text)
            else:
                mid = Message.objects.create(
                    user = r.user,
                    text = PickupThree(i.title),
                    action = 1,
                    order = r,
                    product = i,
                    get_or_return = 2,
                    ownerorclient = 2,
                    words = [i.title]
                )
                send_push(r.user, mid.text)
    return "ok"
    

    
        
