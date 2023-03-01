from acc.signals import user_notify_7_days
from crm.models import Customer
from elk.celery import app as celery


@celery.task
def notify_7_days():
    """
    If the student has not had any classes in the last week, we send a reminder email
    """
    for student in Customer.objects.all():
        classes_last_7_days = student.classes.classes_last_7_days()
        if classes_last_7_days.count() == 0:
            user_notify_7_days.send(sender=notify_7_days, user=student.user)
