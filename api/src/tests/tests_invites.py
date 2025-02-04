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
def test_get_invites_page(client, admin_user):
    success_login = client.login(email='admin@admin.org', password='admin')

    response = client.get(reverse('invites:create_invite'))

    assert success_login
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_invite(client, admin_user):
    success_login = client.login(email='admin@admin.org', password='admin')

    response = client.post(reverse('invites:create_invite'))

    response_data = json.loads(response.content)
    print(Invite.objects.first().link[-22:])

    assert success_login
    assert response.status_code == 200
    assert response_data['message'] == 'success'
    assert Invite.objects.count() == 1


@pytest.mark.django_db
def test_delete_invite(client, admin_user):
    success_login = client.login(email='admin@admin.org', password='admin')
    assert success_login
    response = client.post(reverse('invites:create_invite'))
    assert response.status_code == 200
    invite = Invite.objects.first()
    assert invite is not None

    response = client.delete(reverse('invites:delete_invite', args=[invite.id]))

    response_data = json.loads(response.content)
    print(response_data)

    assert response.status_code == 200
    assert not Invite.objects.filter(id=invite.id).exists()
    assert response_data['status'] == 'success'
    assert response_data['message'] == 'Invite deleted'
