from abc import abstractmethod
from typing import Any

from src.domain.base import BaseRepository

from .dtos import CreateTeamDTO, TeamDTO


class ITeamRepository(BaseRepository):

    @abstractmethod
    def create(self, dto: CreateTeamDTO) -> tuple[None, Any] | TeamDTO:
        raise NotImplementedError

    @abstractmethod
    def update(
        self, pk: int, dto: TeamDTO
    ) -> [tuple[None, Any] | TeamDTO, Any]:
        raise NotImplementedError
