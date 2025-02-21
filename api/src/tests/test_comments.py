import pytest
import json
from django.urls import reverse

from .factories import TaskFactory, CommentFactory

from src.models.projects import Comment


@pytest.mark.django_db
def test_create_comment_view(authenticated_client):
    task = TaskFactory()

    new_comment_data = {
        "task_id": task.id,
        "comment": "This is a test comment",
    }
    # текст с пробелами валидацию не проходит
    response = authenticated_client.post(
        reverse('projects:create_comment', args=[task.id]),
        data=new_comment_data,
    )

    assert response.status_code == 201
    assert response.json()["status"] == "success"
    assert Comment.objects.count() == 1
    assert Comment.objects.first().comment == "This is a test comment"


@pytest.mark.django_db
def test_update_comment_view(authenticated_client):
    comment = CommentFactory(comment="Old comment")

    updated_comment_data = {
        "comment": "Updated comment",
    }
    # текст с пробелами валидацию не проходит
    response = authenticated_client.post(
        reverse('projects:update_comment', args=[comment.id]),
        data=updated_comment_data,
    )

    assert response.status_code == 201
    comment.refresh_from_db()
    assert comment.comment == "Updated comment"


@pytest.mark.django_db
def test_delete_comment_view(authenticated_client):
    comment = CommentFactory()

    assert Comment.objects.filter(id=comment.id).exists()

    response = authenticated_client.delete(
        reverse('projects:delete_comment', args=[comment.id])
    )

    assert response.status_code == 200
    assert not Comment.objects.filter(id=comment.id).exists()
