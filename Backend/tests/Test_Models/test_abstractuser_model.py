from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class AbstractUserManagerTestCase(TestCase):
    def test_create_user(self):
        email = "test@example.com"
        user = User.objects.create_user(email=email)

        self.assertEqual(user.email, email)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

    def test_create_superuser(self):
        email = "admin@example.com"
        user = User.objects.create_superuser(email=email)

        self.assertEqual(user.email, email)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_user_invalid_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email="")

    def test_create_user_with_extra_fields(self):
        email = "test@example.com"
        user_details = "Additional user details"
        user = User.objects.create_user(email=email, user_details=user_details)

        self.assertEqual(user.email, email)
        self.assertEqual(user.user_details, user_details)

    def test_create_superuser_with_invalid_fields(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(email="", is_staff=False, is_superuser=False)

        with self.assertRaises(ValueError):
            User.objects.create_superuser(email="admin@example.com", is_staff=False, is_superuser=False)

        with self.assertRaises(ValueError):
            User.objects.create_superuser(email="admin@example.com", is_staff=True, is_superuser=False)

    def test_create_superuser_with_extra_fields(self):
        email = "admin@example.com"
        user_details = "Additional user details"
        user = User.objects.create_superuser(email=email, user_details=user_details)

        self.assertEqual(user.email, email)
        self.assertEqual(user.user_details, user_details)
