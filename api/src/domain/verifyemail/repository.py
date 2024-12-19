import abc

from src.domain.invites.dtos import InviteDTO


class IVerifyemailRepository(abc.ABC):

    @abc.abstractmethod
    def create(self) -> InviteDTO:
        raise NotImplementedError