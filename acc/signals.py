from django.conf import settings
from django.dispatch import Signal, receiver

from mailer.owl import Owl

new_user_registered = Signal(providing_args=['user', 'whom_to_notify'])  # class is just scheduled
user_notify_7_days = Signal(providing_args=['instance'])  # no class for more than 7 days


@receiver(new_user_registered, dispatch_uid='new_user_notify')
def new_user_notify(sender, **kwargs):
    whom_to_notify = kwargs.get('whom', settings.SUPPORT_EMAIL)

    user = kwargs['user']
    owl = Owl(
        template='mail/service/new_user.html',
        ctx={
            'user': user,
        },
        to=[whom_to_notify],
    )
    owl.send()


@receiver(user_notify_7_days, dispatch_uid='notify_7_days')
def new_user_notify(sender, **kwargs):
    whom_to_notify = kwargs.get('whom', settings.SUPPORT_EMAIL)

    user = kwargs['user']
    owl = Owl(
        template='mail/service/reminder_7_days.html',
        ctx={
            'user': user,
        },
        to=[user.email],
        from_email=whom_to_notify,
    )
    owl.send()
