from src.domain.invites.dtos import InviteDTO
from src.domain.invites.entity import InviteEntity
from src.domain.invites.repository import IInviteRepository


class InviteService:
    def __init__(self, repository: IInviteRepository):
        self.__repository = repository

    def create(self):
        return self.__repository.create()

    def get_invites_list(self) -> list[InviteDTO]:
        return self.__repository.get_invites_list()

    def get_invite(self, pk) -> InviteDTO:
        return self.__repository.get_invite_by_id(pk)

    def delete(self, pk):
        self.__repository.delete(pk)

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
        self.__repository.update_status(invite.pk, status)
