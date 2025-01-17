import os
import secrets
from abc import ABC
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.utils import timezone
from src.domain.invites import IInviteRepository, InviteDTO
from src.models.invites import Invite

user = get_user_model()


class InviteRepository(IInviteRepository, ABC):
    model = Invite

    @classmethod
    def exists(cls, pk: int) -> bool:
        return cls.model.objects.filter(id=pk).exists()

    def _invite_orm_to_dto(self, model) -> InviteDTO:
        return InviteDTO(
            pk=model.id,
            link=model.link,
            status=model.status,
            created_at=model.created_at,
            expires_at=model.expires_at,
        )

    def has_permission(self, user_id: int, action: str, obj=None) -> bool:
        """
        Проверка наличия прав у пользователя на выполнение действия.
        :param user_id: ID пользователя
        :param action: код действия (например, "EDIT", "READ", "COMMENT")
        :param obj: объект, для которого проверяются права (например, Meet)
        :return: bool
        """
        content_type = ContentType.objects.get_for_model(self.model)
        # для митов будем считать то нам не надо распределять права по митам
        # поэтому object_id = None
        # object_id = obj.id if obj else None
        object_id = None

        current_user = get_object_or_404(user, pk=user_id)
        permission = current_user.permissions.filter(
            code=action,
            content_type=content_type,
            object_id=object_id,
        ).exists()
        return permission

    def get_by_id(self, invite_id: int):
        invite = get_object_or_404(Invite, pk=invite_id)
        return self._invite_orm_to_dto(invite)

    def get_list(self):
        return [
            self._invite_orm_to_dto(invite)
            for invite in Invite.objects.all().order_by("-created_at")
        ]

    def create(self) -> InviteDTO:
        invite_link = f"{os.getenv('FRONTEND_URL')}/registration/{secrets.token_urlsafe(16)}"
        created_at = timezone.now()
        expires_at = created_at + timedelta(days=7)

        model = self.model(
            link=invite_link,
            created_at=created_at,
            expires_at=expires_at,
        )
        model.save()

        return self._invite_orm_to_dto(model)

    def delete(self, invite_id: int):
        invite = get_object_or_404(Invite, pk=invite_id)
        invite.delete()

    def update_status(self, invite_id: int, status: str):
        invite = get_object_or_404(Invite, pk=invite_id)
        invite.status = status
        invite.save()

    def create_inviteDTO(self, invitation_code):
        link = f"{os.getenv('FRONTEND_URL')}/registration/{invitation_code}"
        objects_invite = self.model.objects.get(link=link)
        return self._invite_orm_to_dto(objects_invite)
