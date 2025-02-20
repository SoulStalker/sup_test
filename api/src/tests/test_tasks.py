import pytest
from django.urls import reverse

from .factories import TaskFactory, FeaturesFactory, ProjectFactory, CustomUserFactory

from src.models.projects import Task


@pytest.mark.django_db
def test_task_list_view(authenticated_client):
    # Создаем несколько задач
    TaskFactory.create_batch(3)

    # Делаем GET-запрос к списку задач
    response = authenticated_client.get(reverse('projects:tasks'))

    # Проверяем статус и контекст
    assert response.status_code == 200
    assert 'tasks' in response.context
    assert response.context['tasks'].count() == 3

@pytest.mark.django_db
def test_create_task_view(authenticated_client):
    # Проверяем, что задач еще нет
    assert Task.objects.count() == 0

    # Создаем фичу и пользователей
    feature = FeaturesFactory()
    contributor = CustomUserFactory()
    responsible = CustomUserFactory()

    # Данные для новой задачи
    new_task_data = {
        "name": "New Task",
        "priority": 1,
        "contributor": contributor.id,
        "responsible": responsible.id,
        "status": "NEW",
        "feature": feature.id,
    }

    # Отправляем POST-запрос на создание
    response = authenticated_client.post(
        reverse('projects:create_task'),
        data=new_task_data,
    )

    # Проверяем статус и факт создания
    assert response.status_code == 200
    assert Task.objects.count() == 1
    assert Task.objects.first().name == "New Task"

@pytest.mark.django_db
def test_edit_task_view(authenticated_client):
    # Создаем задачу
    task = TaskFactory(name="Old Task")

    # Данные для обновления
    updated_task_data = {
        "name": "Updated Task",
    }

    # Отправляем POST-запрос на обновление
    response = authenticated_client.post(
        reverse('projects:edit_tasks', args=[task.id]),
        data=updated_task_data,
    )

    # Проверяем статус и факт обновления
    assert response.status_code == 200
    task.refresh_from_db()
    assert task.name == "Updated Task"

@pytest.mark.django_db
def test_delete_task_view(authenticated_client):
    # Создаем задачу
    task = TaskFactory()

    # Проверяем, что задача существует
    assert Task.objects.filter(id=task.id).exists()

    # Отправляем DELETE-запрос на удаление
    response = authenticated_client.delete(
        reverse('projects:delete_tasks', args=[task.id])
    )

    # Проверяем статус и факт удаления
    assert response.status_code == 200
    assert not Task.objects.filter(id=task.id).exists()