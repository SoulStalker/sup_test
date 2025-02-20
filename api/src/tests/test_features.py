import pytest
from django.urls import reverse

from .factories import FeaturesFactory, ProjectFactory, CustomUserFactory

from src.models.projects import Features


@pytest.mark.django_db
def test_features_list_view(authenticated_client):
    # Создаем несколько фич
    FeaturesFactory.create_batch(3)

    # Делаем GET-запрос к списку фич
    response = authenticated_client.get(reverse('projects:features'))

    # Проверяем статус и контекст
    assert response.status_code == 200
    assert 'features' in response.context
    assert response.context['features'].count() == 3

@pytest.mark.django_db
def test_create_feature_view(authenticated_client):
    # Проверяем, что фич еще нет
    assert Features.objects.count() == 0

    # Создаем проект и пользователя
    project = ProjectFactory()
    responsible = CustomUserFactory()

    # Данные для новой фичи
    new_feature_data = {
        "name": "New Feature",
        "description": "New Feature Description",
        "status": "NEW",
        "responsible": responsible.id,
        "project": project.id,
    }

    # Отправляем POST-запрос на создание
    response = authenticated_client.post(
        reverse('projects:create_features'),
        data=new_feature_data,
    )

    # Проверяем статус и факт создания
    assert response.status_code == 200
    assert Features.objects.count() == 1
    assert Features.objects.first().name == "New Feature"

@pytest.mark.django_db
def test_edit_feature_view(authenticated_client):
    # Создаем фичу
    feature = FeaturesFactory(name="Old Feature")

    # Данные для обновления
    updated_feature_data = {
        "name": "Updated Feature",
    }

    # Отправляем POST-запрос на обновление
    response = authenticated_client.post(
        reverse('projects:edit_features', args=[feature.id]),
        data=updated_feature_data,
    )

    # Проверяем статус и факт обновления
    assert response.status_code == 200
    feature.refresh_from_db()
    assert feature.name == "Updated Feature"

@pytest.mark.django_db
def test_delete_feature_view(authenticated_client):
    # Создаем фичу
    feature = FeaturesFactory()

    # Проверяем, что фича существует
    assert Features.objects.filter(id=feature.id).exists()

    # Отправляем DELETE-запрос на удаление
    response = authenticated_client.delete(
        reverse('projects:delete_features', args=[feature.id])
    )

    # Проверяем статус и факт удаления
    assert response.status_code == 200
    assert not Features.objects.filter(id=feature.id).exists()