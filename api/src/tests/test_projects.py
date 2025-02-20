import pytest
from django.urls import reverse

from .factories import ProjectFactory, CustomUserFactory

from src.models.projects import Project

@pytest.mark.django_db
def test_project_list_view(authenticated_client):
    # Создаем несколько проектов
    ProjectFactory.create_batch(3)

    # Делаем GET-запрос к списку проектов
    response = authenticated_client.get(reverse('projects:projects'))

    # Проверяем статус и контекст
    assert response.status_code == 200
    assert 'projects' in response.context
    assert response.context['projects'].count() == 3

@pytest.mark.django_db
def test_create_project_view(authenticated_client):
    # Проверяем, что проектов еще нет
    assert Project.objects.count() == 0

    # Создаем пользователя
    responsible = CustomUserFactory()

    # Данные для нового проекта
    new_project_data = {
        "name": "New Project",
        "description": "New Project Description",
        "status": "DISCUSSION",
        "responsible": responsible.id,
    }

    # Отправляем POST-запрос на создание
    response = authenticated_client.post(
        reverse('projects:create_project'),
        data=new_project_data,
    )

    # Проверяем статус и факт создания
    assert response.status_code == 200
    assert Project.objects.count() == 1
    assert Project.objects.first().name == "New Project"

@pytest.mark.django_db
def test_edit_project_view(authenticated_client):
    # Создаем проект
    project = ProjectFactory(name="Old Project")

    # Данные для обновления
    updated_project_data = {
        "name": "Updated Project",
    }

    # Отправляем POST-запрос на обновление
    response = authenticated_client.post(
        reverse('projects:edit_project', args=[project.id]),
        data=updated_project_data,
    )

    # Проверяем статус и факт обновления
    assert response.status_code == 200
    project.refresh_from_db()
    assert project.name == "Updated Project"

@pytest.mark.django_db
def test_delete_project_view(authenticated_client):
    # Создаем проект
    project = ProjectFactory()

    # Проверяем, что проект существует
    assert Project.objects.filter(id=project.id).exists()

    # Отправляем DELETE-запрос на удаление
    response = authenticated_client.delete(
        reverse('projects:delete_project', args=[project.id])
    )

    # Проверяем статус и факт удаления
    assert response.status_code == 200
    assert not Project.objects.filter(id=project.id).exists()
