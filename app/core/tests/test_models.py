from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTest(TestCase):
    def test_create_user_with_email_successful(self):
        """"test creating a new user with an email is successful"""
        email = 'motmaen73@gmail.com'
        password = 'TEST_PASS'
        user = get_user_model().objects.create_user(email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'motmaen73@gmaIL.com'
        password = 'TEST_PASS'
        user = get_user_model().objects.create_user(email=email, password=password)
        self.assertEqual(user.email, email.lower())

    def test_new_invalid_email(self):
        """Test creating user with no email raises error """
        with self.assertRaises(ValueError):
            password = 'TEST_PASS'
            get_user_model().objects.create_user(email=None, password=password)

    def test_create_new_super_user(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser('motmaen73@gmail.com', 'test123')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
