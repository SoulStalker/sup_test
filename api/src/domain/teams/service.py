from typing import Any

from src.domain.base import BaseService

from .dtos import CreateTeamDTO, TeamDTO
from .repository import ITeamRepository


class TeamService(BaseService):
    def __init__(self, repository: ITeamRepository):
        self._repository = repository

    def create(self, dto: CreateTeamDTO) -> [tuple[None, Any] | TeamDTO, Any]:
        entity = CreateTeamDTO(name=dto.name, participants=dto.participants)
        return self.validate_and_save(entity, self._repository, dto)

    def update(
        self, pk: int, dto: TeamDTO
    ) -> [tuple[None, Any] | TeamDTO, Any]:
        entity = TeamDTO(
            id=dto.id, name=dto.name, participants=dto.participants
        )
        return self.validate_and_update(entity, self._repository, dto, pk)
