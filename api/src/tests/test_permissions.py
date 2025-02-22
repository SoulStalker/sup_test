import pytest
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from .factories import PermissionFactory

from src.models.models import Permission


@pytest.mark.django_db
def test_permissions_list_view(authenticated_client):
    PermissionFactory.create_batch(5)

    response = authenticated_client.get(reverse("users:permissions"))

    assert response.status_code == 200
    assert "permissions" in response.context
    assert len(response.context["permissions"]) == 5


@pytest.mark.django_db
def test_permissions_get_objects(authenticated_client):
    content_type = ContentType.objects.get_for_model(Permission)

    permission = PermissionFactory(content_type=content_type)

    url = reverse("users:get_objects") + f"?content_type_id={content_type.id}"

    response = authenticated_client.get(url)

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, (list, dict))

    assert str(permission.object_id) in data or permission.name in str(data)


@pytest.mark.django_db
def test_create_permission_view(authenticated_client):
    initial_count = Permission.objects.count()

    permission_data = {
        "name": "PermissionTest",
        "code": 1,
        "description": "Test description",
        "content_type": "",
        "object_id": "",
    }
    response = authenticated_client.post(
        reverse("users:create_permission"), data=permission_data
    )

    assert response.status_code == 201
    assert Permission.objects.count() == initial_count + 1
    perm = Permission.objects.get(name="PermissionTest")
    assert perm.code == 1


@pytest.mark.django_db
def test_update_permission_view(authenticated_client):
    permission = PermissionFactory(name="PermissionOld", code=1)

    update_data = {
        "name": "PermissionUpdated",
        "code": 2,
        "description": "Updated description",
        "content_type": "",
        "object_id": "",
    }

    response = authenticated_client.post(
        reverse("users:update_permission", args=[permission.id]),
        data=update_data
    )

    assert response.status_code == 201
    permission.refresh_from_db()
    assert permission.name == "PermissionUpdated"
    assert permission.code == 2


@pytest.mark.django_db
def test_delete_permission_view(authenticated_client):
    permission = PermissionFactory(name="PermissionToDelete", code=3)

    response = authenticated_client.delete(
        reverse("users:delete_permission", args=[permission.id])
    )

    assert response.status_code == 200
    assert Permission.objects.filter(id=permission.id).count() == 0
