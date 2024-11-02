from src.domain.invites.dtos import InviteDTO
from src.domain.invites.repository import IInviteRepository


class InviteService:
    def __init__(self, repository: IInviteRepository):
        self.__repository = repository

    def create(self, dto: InviteDTO):
        self.__repository.create(dto)

    def get_invites_list(self) -> list[InviteDTO]:
        return self.__repository.get_invites_list()

    def get_invite(self, pk) -> InviteDTO:
        return self.__repository.get_invite_by_id(pk)

    def delete(self, pk):
        self.__repository.delete(pk)
