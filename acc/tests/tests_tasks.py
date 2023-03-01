from unittest.mock import patch

from django.core import mail
from freezegun import freeze_time

from acc.tasks import notify_7_days
from elk.utils.testing import ClassIntegrationTestCase
from market.models import Subscription
from products.models import Product1


class TestNotify7Days(ClassIntegrationTestCase):

    @patch('market.signals.Owl')
    def test_notify_7_days_send_email(self, Owl):
        # create entry
        entry = self._create_entry()  # with date 2032, 9, 13, 12, 0
        # create class
        c = self._buy_a_lesson()
        # schedule class and entry
        self._schedule(c, entry)

        # set the time for sending notifications (Tuesday 9:40),
        # task 'notify_7_days' will start now
        with freeze_time('2032-09-14 09:40:00'):
            notify_7_days()
        # create list of email recipients
        out_emails = [outbox.to[0] for outbox in mail.outbox]

        # have emails letters 2 out of 3 customers (except for self.customer)
        self.assertEqual(len(mail.outbox), 3)  # if this test fails, carefully check the timezone you are in
        # host.user have emails
        self.assertIn(self.host.user.email, out_emails)
        # self.customer have emails
        self.assertIn(self.customer.user.email, out_emails)

    @patch('market.signals.Owl')
    def test_notify_7_days_not_send_email(self, Owl):
        # create entry
        entry = self._create_entry()  # with date 2032, 9, 13, 12, 0
        # create class
        c = self._buy_a_lesson()
        # schedule class and entry
        self._schedule(c, entry)
        # set entry.end
        entry.end = self.tzdatetime(2032, 9, 13, 12, 0)
        # create subscription
        self.subscription = Subscription(
            customer=self.customer,
            product=Product1.objects.get(pk=1),
        )
        self.subscription.save()
        # self.subscription.is_fully_used = False

        # assign classes to subscription
        c.subscription = self.subscription
        for i in self.customer.classes.all():
            i.subscription = self.subscription
            i.save()
        # set the time for sending notifications (Tuesday 9:40),
        # task 'notify_7_days' will start now
        with freeze_time('2032-09-14 09:40:00'):
            notify_7_days()
        # create list of email recipients
        out_emails = [outbox.to[0] for outbox in mail.outbox]

        # have emails letters 2 out of 3 customers (except for self.customer)
        self.assertEqual(len(mail.outbox), 2)  # if this test fails, carefully check the timezone you are in
        # host.user have emails
        self.assertIn(self.host.user.email, out_emails)
        # self.customer don't have emails
        self.assertNotIn(self.customer.user.email, out_emails)

    @patch('market.signals.Owl')
    def test_notify_7_days_send_email_without_subscription(self, Owl):
        # create entry
        entry = self._create_entry()  # with date 2032, 9, 13, 12, 0
        # create class
        c = self._buy_a_lesson()
        # schedule class and entry
        self._schedule(c, entry)
        # set entry.end
        entry.end = self.tzdatetime(2032, 9, 13, 12, 0)
        # set the time for sending notifications (Tuesday 9:40),
        # task 'notify_7_days' will start now
        with freeze_time('2032-09-14 09:40:00'):
            notify_7_days()
        # create list of email recipients
        out_emails = [outbox.to[0] for outbox in mail.outbox]

        # have emails letters 2 out of 3 customers (except for self.customer)
        self.assertEqual(len(mail.outbox), 3)  # if this test fails, carefully check the timezone you are in
        # host.user have emails
        self.assertIn(self.host.user.email, out_emails)
        # self.customer have emails
        self.assertIn(self.customer.user.email, out_emails)
