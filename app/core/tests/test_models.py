from django.contrib.auth import get_user_model
from django.test import TestCase

class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        #A test for creating a user instance in user model
        email = 'abc@abcmail.com'
        password = 'TestPassword121'
        user = get_user_model().objects.create_user(email = email,password = password)

        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        email = 'abc@ABCMAIL.COM'
        user = get_user_model().objects.create_user(email,'test123')
        self.assertEqual(user.email,email.lower())

    def test_new_user_invalid_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None,'test123')
    
    def test_create_new_super_user(self):
        user = get_user_model().objects.create_superuser('abc@abcmail.com','test123')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)