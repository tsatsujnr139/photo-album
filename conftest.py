import pytest
from rest_framework.test import APIClient

from users.tests.test_views import sample_user, create_user


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_user(db):
    user = sample_user()
    return create_user(**user)
