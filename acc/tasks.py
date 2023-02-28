from acc.signals import user_notify_7_days
from crm.models import Customer
from elk.celery import app as celery


@celery.task
def notify_7_days():
    for student in Customer.objects.all():
        classes_last_7_days = student.classes.classes_last_7_days()
        if not classes_last_7_days.count():
            user_notify_7_days.send(sender=notify_7_days, user=student.user)
