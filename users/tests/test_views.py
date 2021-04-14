import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse('users:create')
TOKEN_URL = reverse('users:token')
OWN_URL = reverse('users:self')


def create_user(**params):
    """create a user"""
    return get_user_model().objects.create_user(**params)


def sample_user():
    return {
        'email': 'user@email.com',
        'password': 'password123',
        'first_name': 'test',
        'last_name': 'name',
    }


@pytest.mark.django_db
class TestPublicUserAPIs:
    """test publicly accessible api's"""

    def test_create_user_successfully(self, api_client):
        """test creating an user with valid payload successfully"""
        payload = sample_user()

        res = api_client.post(CREATE_USER_URL, payload)
        assert res.status_code == status.HTTP_201_CREATED
        user = get_user_model().objects.get(**res.data)
        assert user.check_password(payload['password']) is True
        assert 'password' not in res.data

    def test_create_user_with_invalid_payload(self, api_client):
        """test creating a user with invalid payload fails"""

        payload = {
            'email': '',
            'password': ''
        }
        res = api_client.post(CREATE_USER_URL, payload)
        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_creating_existing_user(self, api_client):
        """test creating user that already exists fails"""
        payload = sample_user()
        create_user(**payload)

        res = api_client.post(CREATE_USER_URL, payload)
        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_password_too_short(self, api_client):
        """test creating user with password less than 5 characters fails """
        payload = {
            'email': 'user@email.com',
            'password': 'pass'
        }

        res = api_client.post(CREATE_USER_URL, payload)
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        assert user_exists is False

    def test_create_token_successfully(self, api_client):
        """test creating a token when valid user logs in"""
        payload = sample_user()
        create_user(**payload)

        res = api_client.post(TOKEN_URL, payload)
        assert res.status_code == status.HTTP_200_OK
        assert 'token' in res.data

    def test_create_token_for_invalid_user_details(self, api_client):
        """test creating token for invalid user credentials"""
        payload = {
            'email': 'user@email.com',
            'password': 'ppp'
        }
        user = sample_user()
        create_user(**user)
        res = api_client.post(TOKEN_URL, payload)
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        assert 'token' not in res.data

    def test_create_token_for_non_existent_user(self, api_client):
        """test creating token for user that does not exist"""
        payload = sample_user()
        res = api_client.post(TOKEN_URL, payload)
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        assert 'token' not in res.data

    def test_create_token_required_fields(self, api_client):
        """test that required field must be passed to create token"""
        payload = {
            'email': 'user@email.com',
            'password': ''
        }
        res = api_client.post(TOKEN_URL, payload)
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        assert 'token' not in res.data

    def test_retrieve_user_unauthorized(self, api_client):
        """test that authentication is required to access a profile"""
        res = api_client.get(OWN_URL)

        assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestPrivateUserAPIs:
    """test api's that require authentication"""

    def test_retrieve_own_profile_successfully(self, api_client, test_user):
        """test that authenticated user is able to access their profile"""
        api_client.force_authenticate(user=test_user)
        res = api_client.get(OWN_URL)

        assert res.status_code == status.HTTP_200_OK
        assert res.data == {
            'email': test_user.email,
            'first_name': test_user.first_name,
            'last_name': test_user.last_name
        }

    def test_post_not_allowed_for_own_profile(self, api_client, test_user):
        """test that POST method is not allowed for retrieve profile url"""
        api_client.force_authenticate(user=test_user)
        res = api_client.post(OWN_URL, {})

        assert res.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_own_profile_update(self, api_client, test_user):
        """test updating profile for authenticated user"""
        payload = {
            'first_name': 'new',
            'password': 'new password'
        }
        api_client.force_authenticate(user=test_user)
        res = api_client.patch(OWN_URL, payload)
        test_user.refresh_from_db()
        assert res.status_code, status.HTTP_200_OK
        assert test_user.first_name == payload['first_name']
        assert test_user.check_password(payload['password']) is True
