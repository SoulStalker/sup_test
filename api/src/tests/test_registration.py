import pytest
import json
from django.urls import reverse
from django.contrib.auth import get_user_model

from src.models.invites import Invite

User = get_user_model()


@pytest.mark.django_db
def test_get_registration_page(client, admin_user):
    success_admin_login = client.login(email='admin@admin.org', password='admin')
    assert success_admin_login

    creating_invite = client.post(reverse('invites:create_invite'))
    assert creating_invite.status_code == 200

    response = client.get(reverse('registration:registration', args=[Invite.objects.first().link[-22:]]))

    assert response.status_code == 200


@pytest.mark.django_db
def test_post_registration_page(client, admin_user):
    success_admin_login = client.login(email='admin@admin.org', password='admin')
    assert success_admin_login

    creating_invite = client.post(reverse('invites:create_invite'))
    assert creating_invite.status_code == 200

    data = {
        "name": "first_name",
        "surname": "last_name",
        "email": "user1@example.com",
        "password1": "Password_123",
        "password2": "Password_123",
        "tg_name": "tg_name_1",
        "tg_nickname": "tg_nickname_1",
        "google_meet_nickname": "google_meet_1",
        "gitlab_nickname": "gitlab_1",
        "github_nickname": "github_1",
    }

    response = client.post(reverse(
        'registration:registration',
        args=[Invite.objects.first().link[-22:]]
    ), data=data)
    response_data = json.loads(response.content)

    assert response.status_code == 201
    assert response_data['status'] == 'success'
    assert User.objects.filter(email='user1@example.com').exists()
    assert User.objects.filter(email='user1@example.com').count() == 1
