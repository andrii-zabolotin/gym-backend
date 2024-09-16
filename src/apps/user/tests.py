from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from phonenumber_field.phonenumber import PhoneNumber


class UsersManagersTest(TestCase):
    def setUp(self):
        self.User = get_user_model()

    def test_create_user(self):
        user = self.User.objects.create_user(
            phone=PhoneNumber.from_string("+380666657664"),
            email="normal@user.com",
            password="foo",
            first_name="foo",
            last_name="boo",
            sex="Male",
            birth_date=date(2004, 12, 12),
        )
        self.assertEqual(user.email, "normal@user.com")
        self.assertEqual(user.phone.as_e164, "+380666657664")
        self.assertEqual(user.first_name, "foo")
        self.assertEqual(user.last_name, "boo")
        self.assertEqual(user.sex, "Male")
        self.assertEqual(user.birth_date, "12-12-2004")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_massagist)
        self.assertFalse(user.is_trainer)
        self.assertFalse(user.is_superuser)
        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass

    def test_create_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            self.User.objects.create_user(
                phone=PhoneNumber.from_string("+380666657664"),
                email="",
                password="foo",
                first_name="foo",
                last_name="boo",
                sex="Male",
                birth_date=date(2004, 12, 12),
            )

    def test_create_user_without_phone_raises_error(self):
        with self.assertRaises(ValueError):
            self.User.objects.create_user(
                phone=None,
                email="normal@user.com",
                password="foo",
                first_name="foo",
                last_name="boo",
                sex="Male",
                birth_date=date(2004, 12, 12),
            )

    def test_create_user_without_password_raises_error(self):
        with self.assertRaises(ValueError):
            self.User.objects.create_user(
                phone=PhoneNumber.from_string("+380666657664"),
                email="normal@user.com",
                password="",
                first_name="foo",
                last_name="boo",
                sex="Male",
                birth_date=date(2004, 12, 12),
            )

    def test_create_user_with_invalid_phone_raises_error(self):
        with self.assertRaises(ValueError):
            self.User.objects.create_user(
                phone="+380669",
                email="normal@user.com",
                password="foo",
                first_name="foo",
                last_name="boo",
                sex="Male",
                birth_date=date(2004, 12, 12),
            )

    def test_create_superuser(self):
        admin_user = self.User.objects.create_superuser(
            phone=PhoneNumber.from_string("+380665557554"),
            email="super@user.com",
            password="foo",
            first_name="Admin",
            last_name="User",
            sex="Female",
            birth_date=date(1985, 12, 20),
        )
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertFalse(admin_user.is_massagist)
        self.assertFalse(admin_user.is_trainer)
        self.assertTrue(admin_user.is_superuser)
        try:
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass

    def test_create_superuser_without_flag_error(self):
        with self.assertRaises(ValueError):
            self.User.objects.create_superuser(
                phone=PhoneNumber.from_string("+380665557554"),
                email="super@user.com",
                password="foo",
                first_name="Admin",
                last_name="User",
                sex="Female",
                birth_date=date(1985, 12, 20),
                is_superuser=False
            )
