import abc

from src.domain.invites.dtos import InviteDTO


class IInviteRepository(abc.ABC):
    @abc.abstractmethod
    def get_invite_by_id(self, invite_id: int):
        pass

    @abc.abstractmethod
    def get_invites_list(self) -> list[InviteDTO]:
        pass

    @abc.abstractmethod
    def create(self) -> InviteDTO:
        pass

    @abc.abstractmethod
    def delete(self, invite_id: int):
        pass
