import abc
from typing import Any

from .dtos import CreateTeamDTO, TeamDTO


class ITeamRepository(abc.ABC):
    @abc.abstractmethod
    def get_team_list(self) -> list[TeamDTO]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_team_by_id(self, team_id: int) -> TeamDTO:
        raise NotImplementedError

    @abc.abstractmethod
    def create(self, dto: CreateTeamDTO) -> tuple[None, Any] | TeamDTO:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, dto: TeamDTO) -> [tuple[None, Any] | TeamDTO, Any]:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, team_id: int):
        raise NotImplementedError
