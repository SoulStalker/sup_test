import pytest
from django.urls import reverse

from .factories import TaskFactory, TagsFactory, FeaturesFactory, CustomUserFactory

from src.models.projects import Task


@pytest.mark.django_db
def test_task_list_view(authenticated_client):
    TaskFactory.create_batch(3)

    response = authenticated_client.get(reverse('projects:tasks'))

    assert response.status_code == 200
    assert 'tasks' in response.context
    assert len(response.context['tasks']) == 3


@pytest.mark.django_db
def test_create_task_view(authenticated_client):
    assert Task.objects.count() == 0

    feature = FeaturesFactory()
    tags = TagsFactory.create_batch(3)
    contributor = CustomUserFactory()
    responsible = CustomUserFactory()

    new_task_data = {
        "name": "New Task",
        "priority": 1,
        "contributor": contributor.id,
        "responsible": responsible.id,
        "status": "Готов",
        "feature": feature.id,
        "description": "New Task description",
        "tags": [tag.id for tag in tags],
    }

    response = authenticated_client.post(
        reverse('projects:create_task'),
        data=new_task_data,
    )

    assert response.status_code == 201
    assert Task.objects.count() == 1
    assert Task.objects.first().name == "New Task"


@pytest.mark.django_db
def test_edit_task_view(authenticated_client):
    task = TaskFactory(name="Old Task")

    feature = FeaturesFactory()
    tags = TagsFactory.create_batch(3)
    contributor = CustomUserFactory()
    responsible = CustomUserFactory()

    updated_task_data = {
        "name": "New Task",
        "priority": 1,
        "contributor": contributor.id,
        "responsible": responsible.id,
        "status": "Готов",
        "feature": feature.id,
        "description": "New Task description",
        "tags": [tag.id for tag in tags],
    }

    response = authenticated_client.post(
        reverse('projects:edit_tasks', args=[task.id]),
        data=updated_task_data,
    )

    assert response.status_code == 201
    task.refresh_from_db()
    assert task.name == "New Task"


@pytest.mark.django_db
def test_delete_task_view(authenticated_client):
    task = TaskFactory()

    assert Task.objects.filter(id=task.id).exists()

    response = authenticated_client.delete(
        reverse('projects:delete_tasks', args=[task.id])
    )

    assert response.status_code == 200
    assert not Task.objects.filter(id=task.id).exists()
