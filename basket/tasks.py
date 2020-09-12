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

from huey.contrib.djhuey import db_periodic_task, db_task

# @periodic_task(run_every=timedelta(seconds=10))
@db_periodic_task(crontab(minute=0, hour=9))
def send_notifiction():
    print('Here I\’m')
    
    # send_push()
    p = Product.objects.filter(is_rented=True, count_day__isnull=False, rented_obj__is_rented=True)
    for i in p:
        r = i.rented_obj.all()[0]
        rented = datetime.strptime(str(r.rented_day), '%Y-%m-%d')
        deadline = rented + timedelta(i.count_day)
        if datetime.now() < deadline:
            days_left = datetime.now()-deadline
            # print(abs(days_left.days))
            if abs(days_left.days) == 1:
                # a.append(i)
                if r.return_product == 1:
                    mid = Message.objects.create(
                        user = r.user,
                        text = deliverThree(i.title),
                        action = 2,
                        order = r,
                        product = i,
                        get_or_return = 2,
                        ownerorclient = 2
                    )
                else:
                    mid = Message.objects.create(
                        user = r.user,
                        text = PickupThree(i.title),
                        action = 1,
                        order = r,
                        product = i,
                        get_or_return = 2,
                        ownerorclient = 2
                    )
    return "ok"
    

    
        
