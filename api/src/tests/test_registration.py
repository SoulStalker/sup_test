import pytest
import json
from django.urls import reverse
from django.test.client import Client
from django.contrib.auth import get_user_model

from src.models.invites import Invite
from src.domain.invites.dtos import InviteDTO

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


@pytest.mark.django_db
def test_get_registration_page(client, admin_user):
    success_admin_login = client.login(email='admin@admin.org', password='admin')
    assert success_admin_login

    creating_invite = client.post(reverse('invites:create_invite'))
    assert creating_invite.status_code == 200

    response = client.get(reverse('registration:registration', args=[Invite.objects.first().link[-22:]]))

    assert response.status_code == 200
