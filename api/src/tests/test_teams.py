import pytest
from django.urls import reverse

from .factories import TeamFactory, CustomUserFactory

from src.models.models import Team


@pytest.mark.django_db
def test_team_list_view(authenticated_client):
    TeamFactory.create_batch(3)

    response = authenticated_client.get(reverse('teams:teams'))

    assert response.status_code == 200
    assert 'teams' in response.context
    assert len(response.context['teams']) == 3


@pytest.mark.django_db
def test_team_create_view(authenticated_client):
    assert Team.objects.count() == 0

    user1 = CustomUserFactory(team=None)
    user2 = CustomUserFactory(team=None)
    new_team_data = {
        "name": "New Team",
        "participants": [user1.pk, user2.pk]
    }

    response = authenticated_client.post(reverse('teams:create_team'), data=new_team_data)

    assert response.status_code == 201
    assert Team.objects.count() == 1
    assert Team.objects.first().name == "New Team"


@pytest.mark.django_db
def test_team_update_view(authenticated_client):
    team = TeamFactory(name="Old Team")

    user1 = CustomUserFactory(team=None)
    user2 = CustomUserFactory(team=None)
    updated_team_data = {
        "name": "Updated Team",
        "participants": [user1.pk, user2.pk]
    }

    response = authenticated_client.post(
        reverse('teams:update_team', args=[team.id]),
        data=updated_team_data
    )

    assert response.status_code == 201
    assert response.json()["status"] == "success"

    # Проверяем, что команда обновилась в базе данных
    team.refresh_from_db()
    assert team.name == "Updated Team"


@pytest.mark.django_db
def test_team_delete_view(authenticated_client):
    team = TeamFactory()

    assert Team.objects.filter(id=team.id).exists()

    response = authenticated_client.delete(
        reverse('teams:delete_team', args=[team.id])
    )

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["message"] == "Team deleted"

    assert not Team.objects.filter(id=team.id).exists()
