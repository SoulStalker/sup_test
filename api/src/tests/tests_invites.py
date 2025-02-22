import pytest
import json
from django.urls import reverse
from django.contrib.auth import get_user_model

from src.models.invites import Invite

User = get_user_model()


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

    assert response.status_code == 200
    assert not Invite.objects.filter(id=invite.id).exists()
    assert response_data['status'] == 'success'
    assert response_data['message'] == 'Invite deleted'
