from django.contrib.auth import get_user_model
from django.test import TestCase


class ModelTests(TestCase):

    def test_create_user_with_email_successfully(self):
        email = "Ansuman@YOPmail.com"
        password = "kathmandu@123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password)
        self.assertEqual(user.email, email.lower())
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """checks if the user email is normalized"""
        email = "ansuman@YOPMAIL.com"
        user = get_user_model().objects.create_user(
            email=email, password="ansuman123"
        )
        self.assertEqual(email.lower(), user.email)

    def test_new_user_valid_email(self):
        """Tests if the new user email is not None"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "test@123")

    def test_new_superuser_creation(self):
        """Tests the new superuser created for is_staff and is_superuser
        permissions"""

        user = get_user_model().objects.create_superuser(
            email="ansuman@yopmail.com",
            password='test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
