from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from apps.subscriptions.models import Subscription, UserSubscription
from apps.user.models import CustomUser


class SubscriptionModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            email='testuser@example.com',
            password='password123',
            first_name='Test',
            last_name='User',
            sex="M",
            birth_date="1990-01-01",
        )

        self.subscription = Subscription.objects.create(
            name='Premium Membership',
            subscription_type='personal',
            validity_period=30,
            available_number_of_visits=10,
            price=1000
        )

    def test_subscription_creation(self):
        self.assertEqual(self.subscription.name, 'Premium Membership')
        self.assertEqual(self.subscription.subscription_type, 'personal')
        self.assertEqual(self.subscription.validity_period, 30)
        self.assertEqual(self.subscription.available_number_of_visits, 10)
        self.assertEqual(self.subscription.price, 1000)
        self.assertIsNotNone(self.subscription.created_at)
        self.assertIsNotNone(self.subscription.updated_at)


class UserSubscriptionModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            email='testuser@example.com',
            password='password123',
            first_name='Test',
            last_name='User',
            sex="M",
            birth_date="1990-01-01",
        )

        self.subscription = Subscription.objects.create(
            name='Premium Membership',
            subscription_type='personal',
            validity_period=30,
            available_number_of_visits=10,
            price=1000
        )

        self.user_subscription = UserSubscription.objects.create(
            user=self.user,
            subscription=self.subscription
        )

    def test_user_subscription_creation(self):
        self.assertEqual(self.user_subscription.user, self.user)
        self.assertEqual(self.user_subscription.subscription, self.subscription)
        self.assertIsNotNone(self.user_subscription.purchase_at)
        self.assertIsInstance(self.user_subscription.purchase_at, timezone.datetime)

    def test_user_subscription_expiration_at(self):
        expected_expiration_date = self.user_subscription.purchase_at + timedelta(
            days=self.subscription.validity_period)
        self.assertEqual(self.user_subscription.expiration_at.date(), expected_expiration_date.date())
