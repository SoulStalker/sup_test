from abc import ABC

from django.shortcuts import get_object_or_404
from src.domain.invites.dtos import InviteDTO
from src.domain.invites.repository import IInviteRepository
from src.models.invites import Invite


class InviteRepository(IInviteRepository, ABC):
    model = Invite

    def _invite_orm_to_dto(self, model):
        return InviteDTO(
            link=model.link,
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def get_invite_by_id(self, invite_id: int):
        # todo to DTO
        return get_object_or_404(Invite, pk=invite_id)

    def get_invites_list(self):
        # todo to list DTO
        return list(Invite.objects.all().order_by("-created_at"))

    def create(self, dto: InviteDTO) -> InviteDTO:
        model = self.model(
            link=dto.link,
            status=dto.status,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )

        model.save()
        return self._invite_orm_to_dto(model)

    def delete(self, invite_id: int):
        invite = get_object_or_404(Invite, pk=invite_id)
        invite.delete()
