import pytest
from django.test import Client
from django.contrib.auth import get_user_model

from .factories import CustomUserFactory

User = get_user_model()


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def admin_user(db):
    user = User.objects.create_user(
        email='admin@admin.org',
        password='admin',
    )
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.save()
    return user


@pytest.fixture
def authenticated_client(client, admin_user):
    client.login(email='admin@admin.org', password='admin')
    return client
