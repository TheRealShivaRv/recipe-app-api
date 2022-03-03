from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


def create_user(**params):
    get_user_model().objects.create_user(**params)


CREATE_USER_URL = reverse('users:create')
TOKEN_URL = reverse('users:token')


class PublicUserApiTests(TestCase):
    def setUp(self):  # Setting up client object
        self.client = APIClient()

    def test_create_user_success(self):  # Creating user test
        payload = {
            'email': "test@test.com",
            'password': "123456",
            'name': "Test Name"
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):  # Checking if the user already exists
        payload = {
            'email': "test@test.com",
            'password': "123456",
            'name': "Test Name"
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # Checking if  the password is too short
    def test_user_password_too_short(self):
        payload = {
            'email': "test@test.com",
            'password': "pw",
            'name': "Test Name"
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']).exists()
        self.assertFalse(user_exists)

    # Creating token for an existing user

    def test_create_token_for_user(self):
        payload = {
            'email': "test@test.com",
            'password': "123456"
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    # Creating token when the user credentials are invalid
    def test_create_token_invalid_credentials(self):
        payload = {
            'email': "test@test.com",
            'password': "123456"
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, {'email': "test@test.com",
                                           'password': "123"})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    # Creating token for non existing user
    def test_create_token_no_user(self):
        payload = {
            'email': "test@test.com",
            'password': "123456"
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # Creating token for missing fields in login form submission

    def test_create_token_missing_fields(self):
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)
