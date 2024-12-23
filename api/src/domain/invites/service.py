from src.domain.base import BaseService

from .dtos import InviteDTO
from .entity import InviteEntity
from .repository import IInviteRepository


class InviteService(BaseService):
    def __init__(self, repository: IInviteRepository):
        self._repository = repository

    def create(self):
        return self._repository.create()

    def create_inviteDTO(self, invitation_code):
        return self._repository.create_inviteDTO(invitation_code)

    def update_status(self, dto: InviteDTO, status: str = "EXPIRED"):
        invite = InviteEntity(
            pk=dto.pk,
            link=dto.link,
            status=dto.status,
            created_at=dto.created_at,
            expires_at=dto.expires_at,
        )
        if status == "EXPIRED":
            status = invite.expire_status()
        elif status == "USED":
            status = invite.use_invite()
        else:
            return "Invalid status"
        self._repository.update_status(invite.pk, status)
