import pytest
import json
from django.urls import reverse
from django.contrib.auth import get_user_model

from .factories import CustomUserFactory

from src.models.invites import Invite
from src.models.verifyemail import VerifyEmail

User = get_user_model()


@pytest.mark.django_db
def test_post_verify_email(client, admin_user):
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

    creating_user = client.post(reverse(
        'registration:registration',
        args=[Invite.objects.first().link[-22:]]
    ), data=data)
    assert creating_user.status_code == 201

    user = User.objects.get(email='user1@example.com')
    data = {
        "email": "user1@example.com",
        "password": "Password_123"
    }
    # не меняется статус, хз как реализовать переход по ссылке, чтоб статус менялся
    # user.is_active = True
    # user.save()
    response = client.get(reverse('verifyemail:verifyemail', args=[VerifyEmail.objects.last().link[-4:]]), data=data)
    # print(user.is_active)
    # print(VerifyEmail.objects.last())
    # print("Response content:", response.content.decode())
    assert response.status_code == 200
