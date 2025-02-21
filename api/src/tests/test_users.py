import pytest
from django.urls import reverse

from .factories import CustomUserFactory, RoleFactory, TeamFactory, PermissionFactory

from src.models.models import CustomUser



@pytest.mark.django_db
def test_users_list_view(authenticated_client):
    CustomUserFactory.create_batch(5)

    response = authenticated_client.get(reverse("users:users"))

    print("Response status:", response.status_code)

    if response.content:
        print("Response content:", response.content.decode())


    assert response.status_code == 200
    assert "users" in response.context
    assert len(response.context["users"]) > 0


@pytest.mark.django_db
def test_create_user_view(authenticated_client):
    initial_count = CustomUser.objects.count()
    role = RoleFactory()
    team = TeamFactory(participants=None)
    perm1 = PermissionFactory(code=1)
    perm2 = PermissionFactory(code=2)

    user_data = {
        "name": "TestName",
        "surname": "TestSurname",
        "email": "testuser@example.com",
        "password": "Password_123",
        "tg_name": "tgname_test",
        "tg_nickname": "tgnickname_test",
        "google_meet_nickname": "googlemeet_test",
        "gitlab_nickname": "gitlab_test",
        "github_nickname": "github_test",
        "role": role.id,
        "team": team.id,
        "permissions": [perm1.id, perm2.id],
        "is_active": True,
        "is_admin": False,
        "is_superuser": False,
    }

    response = authenticated_client.post(
        reverse("users:create_user"),
        data=user_data
    )

    assert response.status_code == 201
    assert CustomUser.objects.count() == initial_count + 1
    created_user = CustomUser.objects.get(email="testuser@example.com")
    assert created_user.name == "TestName"
    assert created_user.role.id == role.id

@pytest.mark.django_db
def test_update_user_view(authenticated_client):
    user = CustomUserFactory(name="OldName")

    update_data = {
        "name": "NewName",
        "surname": user.surname,
        "email": user.email,
        "password": user.password,
        "tg_name": user.tg_name,
        "tg_nickname": user.tg_nickname,
        "google_meet_nickname": user.google_meet_nickname,
        "gitlab_nickname": user.gitlab_nickname,
        "github_nickname": user.github_nickname,
        "role": user.role.id,
        "team": user.team.id if user.team else "",
        "permissions": [],
        "is_active": user.is_active,
        "is_admin": user.is_admin,
        "is_superuser": user.is_superuser,
    }
    response = authenticated_client.post(
        reverse("users:update_user", args=[user.id]),
        data=update_data
    )


    assert response.status_code == 201
    user.refresh_from_db()
    assert user.name == "NewName"


@pytest.mark.django_db
def test_password_change_view(authenticated_client):
    user = CustomUserFactory()
    user.set_password("Oldpassword_123")
    user.save()

    authenticated_client.login(email=user.email, password="Oldpassword_123")

    new_password = "NewPassword_456"
    data = {
        "current_password": "Oldpassword_123",
        "new_password1": new_password,
        "new_password2": new_password,
    }

    response = authenticated_client.post(reverse("users:update_password"), data=data)

    assert response.status_code in (200, 302)
    user.refresh_from_db()
    assert user.check_password(new_password)
