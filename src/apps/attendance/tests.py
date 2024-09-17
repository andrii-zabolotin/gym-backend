from django.test import TestCase
from django.utils import timezone

from apps.attendance.models import Attendance, AttendanceTraining
from apps.subscriptions.models import Subscription, UserSubscription
from apps.trainings.models import Training, TrainingUser
from apps.user.models import CustomUser


class AttendanceTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            phone="+1234567890",
            email="testuser@example.com",
            first_name="Test",
            last_name="User",
            sex="M",
            birth_date="1990-01-01",
            password="testpassword"
        )

        self.trainer = CustomUser.objects.create_user(
            phone="+1234567891",
            email="trainer@example.com",
            first_name="Trainer",
            last_name="User",
            sex="M",
            birth_date="1985-05-15",
            password="trainerpassword",
            is_trainer=True
        )

        self.subscription = Subscription.objects.create(
            name="Group plan",
            subscription_type="group",
            validity_period=30,
            available_number_of_visits=10,
            price=500
        )

        self.user_subscription = UserSubscription.objects.create(
            user=self.user,
            subscription=self.subscription
        )

        self.training = Training.objects.create(
            description="Test Yoga Session",
            training_type="yoga",
            trainer=self.trainer,
            date=timezone.now().date(),
            start_time="10:00:00",
            end_time="11:00:00",
            max_participants=10
        )

    def test_create_training_user(self):
        # Тест на создание связи между тренировкой и пользователем (участником)
        training_user = TrainingUser.objects.create(
            user_subscription=self.user_subscription,
            training=self.training
        )
        self.assertEqual(training_user.user_subscription, self.user_subscription)
        self.assertEqual(training_user.training, self.training)

    def test_create_attendance(self):
        # Тест на создание посещения
        attendance = Attendance.objects.create(
            user_subscription=self.user_subscription
        )
        self.assertEqual(attendance.user_subscription, self.user_subscription)

    def test_create_attendance_training(self):
        # Тест на создание посещения тренировки
        attendance = Attendance.objects.create(
            user_subscription=self.user_subscription
        )
        attendance_training = AttendanceTraining.objects.create(
            attendance=attendance,
            training=self.training
        )
        self.assertEqual(attendance_training.attendance, attendance)
        self.assertEqual(attendance_training.training, self.training)

    def test_unique_constraint(self):
        # Создание посещения
        attendance = Attendance.objects.create(user_subscription=self.user_subscription)

        # Создание первой записи в AttendanceTraining
        AttendanceTraining.objects.create(attendance=attendance, training=self.training)

        # Проверка уникальности (должно вызвать ошибку, если создать ту же запись)
        with self.assertRaises(Exception):
            AttendanceTraining.objects.create(attendance=attendance, training=self.training)
