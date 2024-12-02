import abc

from .dtos import TeamDTO


class ITeamRepository(abc.ABC):
    @abc.abstractmethod
    def get_team_list(self) -> list[TeamDTO]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_team_by_id(self, team_id: int) -> TeamDTO:
        raise NotImplementedError

    @abc.abstractmethod
    def create(self, team_name: str):
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, team_id: int, team_name: str):
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, team_id: int):
        raise NotImplementedError
