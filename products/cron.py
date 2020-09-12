from django_cron import CronJobBase, Schedule
from .views import send_push

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1 # every 2 hours
    RETRY_AFTER_FAILURE_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'products.send_push'    # a unique code

    def do(self):
        send_push()


def MyCronJob():
    send_push()