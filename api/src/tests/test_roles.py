import pytest
from django.urls import reverse

from .factories import RoleFactory


from src.models.models import Role

@pytest.mark.django_db
def test_create_role_view(authenticated_client):
    # Проверяем, что ролей пока нет
    assert Role.objects.count() == 0

    role_data = {
        "name": "RoleTest",   # Название без пробелов, только буквы
        "color": "ff5733",
    }
    response = authenticated_client.post(reverse("users:create_role"), data=role_data)
    response_data = response.json()
    print(response_data)

    assert response.status_code == 201
    assert Role.objects.count() == 1
    created_role = Role.objects.first()
    assert created_role.name == "RoleTest"
    assert created_role.color == "ff5733"

@pytest.mark.django_db
def test_update_role_view(authenticated_client):
    role = RoleFactory(name="RoleOld", color="33ff57")
    update_data = {
        "name": "RoleUpdated",
        "color": "3357ff",
    }
    response = authenticated_client.post(reverse("users:update_role", args=[role.id]), data=update_data)
    response_data = response.json()
    print(response_data)

    assert response.status_code == 201
    role.refresh_from_db()
    assert role.name == "RoleUpdated"
    assert role.color == "3357ff"

@pytest.mark.django_db
def test_delete_role_view(authenticated_client):
    role = RoleFactory(name="RoleToDelete", color="ff33a8")
    response = authenticated_client.delete(reverse("users:delete_role", args=[role.id]))
    response_data = response.json()
    print(response_data)

    assert response.status_code == 200
    assert Role.objects.filter(id=role.id).count() == 0