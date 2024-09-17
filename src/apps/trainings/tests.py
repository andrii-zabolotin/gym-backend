from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from apps.subscriptions.models import Subscription, UserSubscription
from apps.trainings.models import Training, TrainingUser
from apps.user.models import CustomUser


class TrainingModelTest(TestCase):
    def setUp(self):
        self.trainer = CustomUser.objects.create(
            phone="+1234567890",
            email='trainer@example.com',
            password='password123',
            first_name='Trainer',
            last_name='One',
            sex="M",
            birth_date="1990-01-01",
            is_trainer=True
        )

        self.training = Training.objects.create(
            description='Yoga Class',
            training_type='yoga',
            trainer=self.trainer,
            date=timezone.now().date(),
            start_time="10:00:00",
            end_time="11:00:00",
            max_participants=10
        )

    def test_training_creation(self):
        self.assertEqual(self.training.description, 'Yoga Class')
        self.assertEqual(self.training.training_type, 'yoga')
        self.assertEqual(self.training.trainer, self.trainer)
        self.assertEqual(self.training.max_participants, 10)
        self.assertIsNotNone(self.training.created_at)
        self.assertIsNotNone(self.training.updated_at)


class TrainingUserModelTest(TestCase):
    def setUp(self):
        self.trainer = CustomUser.objects.create(
            phone="+1234567890",
            email='trainer@example.com',
            password='password123',
            first_name='Trainer',
            last_name='One',
            sex="M",
            birth_date="1990-01-01",
            is_trainer=True
        )

        self.user = CustomUser.objects.create(
            phone="+1234567899",
            email='user@example.com',
            password='password123',
            first_name='User',
            last_name='One',
            sex="M",
            birth_date="1990-01-01"
        )

        self.subscription = Subscription.objects.create(
            name='Basic Membership',
            subscription_type='group',
            validity_period=30,
            available_number_of_visits=10,
            price=50
        )

        self.user_subscription = UserSubscription.objects.create(
            user=self.user,
            subscription=self.subscription
        )

        self.training = Training.objects.create(
            description='Yoga Class',
            training_type='yoga',
            trainer=self.trainer,
            date=timezone.now().date(),
            start_time="10:00:00",
            end_time="11:00:00",
            max_participants=10
        )

        self.training_user = TrainingUser.objects.create(
            user_subscription=self.user_subscription,
            training=self.training
        )

    def test_training_user_creation(self):
        self.assertEqual(self.training_user.user_subscription, self.user_subscription)
        self.assertEqual(self.training_user.training, self.training)
        self.assertIsNotNone(self.training_user.joined_at)
        self.assertIsInstance(self.training_user.joined_at, timezone.datetime)
