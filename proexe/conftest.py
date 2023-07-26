import pytest
from rest_framework.test import APIClient

from proexe.users.models import User
from proexe.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user(db) -> User:
    return UserFactory()


@pytest.fixture
def api_test_user() -> User:
    return UserFactory.create(
        username="api_test_user",
        email="api_test_user@example.com",
        name="API Test User",
    )


@pytest.fixture
def api_client(api_test_user) -> APIClient:
    api_client = APIClient()
    api_client.force_authenticate(user=api_test_user)

    return api_client
