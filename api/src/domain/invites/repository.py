from abc import abstractmethod

from src.domain.base import BaseRepository

from .dtos import InviteDTO


class IInviteRepository(BaseRepository):
    @abstractmethod
    def create(self, user_id: int) -> InviteDTO:
        raise NotImplementedError

    @abstractmethod
    def update_status(self, invite_id: int, status: str):
        raise NotImplementedError

    @abstractmethod
    def create_inviteDTO(self, invitation_code: str):
        raise NotImplementedError

    def has_permission(self, user_id, param):
        raise NotImplementedError
