from abc import abstractmethod

from src.domain.base import BaseRepository
from src.domain.invites.dtos import InviteDTO


class IInviteRepository(BaseRepository):
    @abstractmethod
    def create(self) -> InviteDTO:
        raise NotImplementedError

    @abstractmethod
    def update_status(self, invite_id: int, status: str):
        raise NotImplementedError

    @abstractmethod
    def create_inviteDTO(self, invitation_code: str):
        raise NotImplementedError
