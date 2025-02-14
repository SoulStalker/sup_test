import pytest
import json
from django.urls import reverse

from .factories import CategoryFactory, MeetFactory, MeetParticipantFactory, CustomUserFactory

from src.models.meets import Category, Meet, MeetParticipant


@pytest.mark.django_db
def test_meet_list_view(authenticated_client):
    MeetFactory.create_batch(3)

    response = authenticated_client.get(reverse('meets:meets'))

    assert response.status_code == 200
    assert 'meets' in response.context
    assert len(response.context['meets']) == 3


@pytest.mark.django_db
def test_create_meet_view(authenticated_client):
    assert Meet.objects.count() == 0

    category = CategoryFactory()
    author = CustomUserFactory()
    responsible = CustomUserFactory()

    new_meet_data = {
        "title": "New Meet",
        "start_time": "2023-10-01T12:00:00Z",
        "category": category.id,
        "author": author.id,
        "responsible": responsible.id,
    }

    response = authenticated_client.post(
        reverse('meets:create_meet'),
        data=new_meet_data,
    )

    assert response.status_code == 201
    assert Meet.objects.count() == 1
    assert Meet.objects.first().title == "New Meet"


@pytest.mark.django_db
def test_edit_meet_view(authenticated_client):
    meet = MeetFactory(title="Old Meet")

    updated_meet_data = {
        "title": "Updated Meet",
        "start_time": "2025-02-14T10:00",
        "category": meet.category.id,
        "responsible": meet.responsible.id,
        "participant_statuses": [],
    }

    response = authenticated_client.post(
        reverse('meets:edit_meet', args=[meet.id]),
        data=updated_meet_data,
    )

    assert response.status_code == 201
    meet.refresh_from_db()
    assert meet.title == "Updated Meet"


@pytest.mark.django_db
def test_delete_meet_view(authenticated_client):
    meet = MeetFactory()

    assert Meet.objects.filter(id=meet.id).exists()

    response = authenticated_client.delete(
        reverse('meets:delete_meet', args=[meet.id])
    )

    assert response.status_code == 200
    assert not Meet.objects.filter(id=meet.id).exists()


@pytest.mark.django_db
def test_add_category_view(authenticated_client, admin_user):
    assert Category.objects.count() == 0

    new_category_data = {
        "category_name": "New Category",
    }

    response = authenticated_client.post(
        reverse('meets:add_category'),
        data=new_category_data,
    )

    assert response.status_code == 200
    assert Category.objects.count() == 1
    assert Category.objects.first().name == "New Category"
