import os
import secrets
from abc import ABC
from datetime import timedelta

from django.shortcuts import get_object_or_404
from django.utils import timezone
from src.domain.invites import IInviteRepository, InviteDTO
from src.models.invites import Invite


class InviteRepository(IInviteRepository, ABC):
    model = Invite

    @classmethod
    def exists(cls, pk: int) -> bool:
        return cls.model.objects.filter(id=pk).exists()

    def _invite_orm_to_dto(self, model) -> InviteDTO:
        # преобразует модель в dto
        return InviteDTO(
            pk=model.id,
            link=model.link,
            status=model.status,
            created_at=model.created_at,
            expires_at=model.expires_at,
        )

    def get_by_id(self, invite_id: int):
        # получение инвайта по id
        invite = get_object_or_404(Invite, pk=invite_id)
        return self._invite_orm_to_dto(invite)

    def get_list(self):
        # получение списка инвайтов
        return [
            self._invite_orm_to_dto(invite)
            for invite in Invite.objects.all().order_by("-created_at")
        ]

    def create(self) -> InviteDTO:
        # создание инвайта
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
        # удаление инвайта
        invite = get_object_or_404(Invite, pk=invite_id)
        invite.delete()

    def update_status(self, invite_id: int, status: str):
        # обновление статуса инвайта
        invite = get_object_or_404(Invite, pk=invite_id)
        invite.status = status
        invite.save()

    def create_inviteDTO(self, invitation_code):
        link = f"{os.getenv('FRONTEND_URL')}/registration/{invitation_code}"
        objects_invite = self.model.objects.get(link=link)
        return self._invite_orm_to_dto(objects_invite)
