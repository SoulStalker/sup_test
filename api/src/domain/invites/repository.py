import abc

from src.domain.invites.dtos import InviteDTO


class IInviteRepository(abc.ABC):
    @abc.abstractmethod
    def get_invite_by_id(self, invite_id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def get_invites_list(self) -> list[InviteDTO]:
        raise NotImplementedError

    @abc.abstractmethod
    def create(self, email) -> InviteDTO:
        print('create repos')
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, invite_id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def update_status(self, invite_id: int, status: str):
        raise NotImplementedError
    
    @abc.abstractmethod
    def create_inviteDTO(self, invitation_code: str):
        raise NotImplementedError
