import pytest
from django.urls import reverse

from .factories import FeaturesFactory, TagsFactory, ProjectFactory, CustomUserFactory

from src.models.projects import Features


@pytest.mark.django_db
def test_features_list_view(authenticated_client):
    FeaturesFactory.create_batch(3)

    response = authenticated_client.get(reverse('projects:features'))

    assert response.status_code == 200
    assert 'features' in response.context
    assert response.context['features'].count() == 3

@pytest.mark.django_db
def test_create_feature_view(authenticated_client):
    assert Features.objects.count() == 0

    project = ProjectFactory()
    responsible = CustomUserFactory()
    tags = TagsFactory.create_batch(3)
    participants = CustomUserFactory.create_batch(3)

    new_feature_data = {
        "name": "New Feature",
        "description": "New Feature Description",
        "status": "Новая",
        "responsible": responsible.id,
        "project": project.id,
        "importance": 1,
        "tags": [tag.id for tag in tags],
        "participants": [user.id for user in participants],
    }

    response = authenticated_client.post(
        reverse('projects:create_features'),
        data=new_feature_data,
    )

    assert response.status_code == 201
    assert Features.objects.count() == 1
    assert Features.objects.first().name == "New Feature"

@pytest.mark.django_db
def test_edit_feature_view(authenticated_client):
    feature = FeaturesFactory(name="Old Feature")

    project = ProjectFactory()
    responsible = CustomUserFactory()
    tags = TagsFactory.create_batch(3)
    participants = CustomUserFactory.create_batch(3)

    updated_feature_data = {
        "name": "New Feature",
        "description": "New Feature Description",
        "status": "Новая",
        "responsible": responsible.id,
        "project": project.id,
        "importance": 1,
        "tags": [tag.id for tag in tags],
        "participants": [user.id for user in participants],
    }

    response = authenticated_client.post(
        reverse('projects:edit_features', args=[feature.id]),
        data=updated_feature_data,
    )

    assert response.status_code == 201
    feature.refresh_from_db()
    assert feature.name == "New Feature"

@pytest.mark.django_db
def test_delete_feature_view(authenticated_client):
    feature = FeaturesFactory()

    assert Features.objects.filter(id=feature.id).exists()

    response = authenticated_client.delete(
        reverse('projects:delete_features', args=[feature.id])
    )

    assert response.status_code == 200
    assert not Features.objects.filter(id=feature.id).exists()