from src.domain.base import BaseService

from .dtos import CreateTeamDTO, TeamDTO
from .repository import ITeamRepository


class TeamService(BaseService):
    def __init__(self, repository: ITeamRepository):
        self._repository = repository

    def create(self, dto: CreateTeamDTO, user_id: int):
        entity = CreateTeamDTO(name=dto.name, participants=dto.participants)
        return self.validate_and_save(entity, self._repository, dto, user_id)

    def update(self, pk: int, dto: TeamDTO, user_id: int):
        entity = TeamDTO(
            id=dto.id, name=dto.name, participants=dto.participants
        )
        return self.validate_and_update(
            entity, self._repository, dto, pk, user_id
        )
