from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    """Helper function to create user in a test"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user using valid payload is valid"""
        payload = {
            'email': 'ansuman@yopmail.com',
            'password': 'testpass',
            'name': 'Ansuman Singh'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(email='ansuman@yopmail.com')
        self.assertTrue(
            user.check_password(payload['password'])
        )
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating a user that already exists fails"""
        payload = {
            'email': 'ansuman@yopmail.com',
            'password': 'test@123',
            'name': 'Ansuman Singh'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test if the password is too short fails"""
        payload = {
            'email': 'ansuman@yopmail.com',
            'password': '123',
            'name': 'Ansuman Singh'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertTrue(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_for_user(self):
        """Test token is generated for valid user"""

        payload = {
            'email': 'ansuman@yopmail.com',
            'password': 'test@123',
            'name': 'Ansuman Singh'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test invalid creds for create token"""
        payload = {
            'email': 'ansuman@yopmail.com',
            'password': 'test@123',
            'name': 'Ansuman Singh'
        }
        create_user(**payload)
        payload = {
            'email': 'ansuman@yopmail.com',
            'password': 'wrong_pass',
            'name': 'Ansuman Singh'
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user doesnot exists"""
        payload = {
            'email': 'not_a_valid@gmail.com',
            'password': 'ansuman@123',
            'name': 'ansuman singh'
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        res = self.client.post(TOKEN_URL, {'email': 'not ', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_authentication_required_for_profile(self):
        """ Tests the me url is accessed only by authenticated user"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTest(TestCase):
    """ Test User api which required authentication """

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='ansuman@yopmail.com',
            password='testpass',
            name='Ansuman Singh'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_user_profile_success(self):
        """ test profile data for me url """
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    def test_post_method_fail(self):
        """ Test POST method is not allowed for profile """
        res = self.client.post(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """ Test updating profile for authenticated user"""

        payload = {'name': 'new name', 'password': 'newPassword123'}
        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
