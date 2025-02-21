import pytest
from django.utils.timezone import localdate
from django.urls import reverse

from .factories import ProjectFactory, CustomUserFactory

from src.models.projects import Project


@pytest.mark.django_db
def test_project_list_view(authenticated_client):
    ProjectFactory.create_batch(3)

    response = authenticated_client.get(reverse('projects:projects'))

    assert response.status_code == 200
    assert 'projects' in response.context
    assert len(response.context['projects']) == 3


@pytest.mark.django_db
def test_create_project_view(authenticated_client):
    assert Project.objects.count() == 0

    responsible = CustomUserFactory()
    participants = CustomUserFactory.create_batch(3)

    new_project_data = {
        "name": "New Project",
        "description": "New Project Description",
        "status": "В обсуждении",
        "responsible": responsible.id,
        "participants": [user.id for user in participants],
        # почему-то автоматически не задается
        "date_created": localdate(),
    }

    response = authenticated_client.post(
        reverse('projects:create_project'),
        data=new_project_data,
    )

    assert response.status_code == 201
    assert Project.objects.count() == 1
    assert Project.objects.first().name == "New Project"


@pytest.mark.django_db
def test_edit_project_view(authenticated_client):
    project = ProjectFactory(name="Old Project")

    responsible = CustomUserFactory()
    participants = CustomUserFactory.create_batch(3)

    updated_project_data = {
        "name": "New Project",
        "description": "New Project Description",
        "status": "В обсуждении",
        "responsible": responsible.id,
        "participants": [user.id for user in participants],
        "date_created": localdate(),
    }

    response = authenticated_client.post(
        reverse('projects:edit_project', args=[project.id]),
        data=updated_project_data,
    )

    assert response.status_code == 201
    project.refresh_from_db()
    assert project.name == "New Project"


@pytest.mark.django_db
def test_delete_project_view(authenticated_client):
    project = ProjectFactory()

    assert Project.objects.filter(id=project.id).exists()

    response = authenticated_client.delete(
        reverse('projects:delete_project', args=[project.id])
    )

    assert response.status_code == 200
    assert not Project.objects.filter(id=project.id).exists()
