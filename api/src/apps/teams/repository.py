from typing import Any

from src.domain.teams.dtos import CreateTeamDTO, TeamDTO
from src.domain.teams.repository import ITeamRepository
from src.models.models import Team


class TeamRepository(ITeamRepository):

    @classmethod
    def _model_team_to_dto(cls, team) -> TeamDTO:
        return TeamDTO(
            id=team.id,
            name=team.name,
            participants=[
                participant.id for participant in team.participants.all()
            ],
        )

    def get_team_list(self) -> list[TeamDTO]:
        teams = Team.objects.all()
        return [
            TeamDTO(id=team.id, name=team.name, participants=team.participants)
            for team in teams
        ]

    def get_team_by_id(self, team_id: int) -> TeamDTO:
        team = Team.objects.get(id=team_id)
        return self._model_team_to_dto(team)

    def create(self, dto: CreateTeamDTO) -> tuple[None, Any] | TeamDTO:
        team = Team(name=dto.name)
        team.save()
        team.participants.set(dto.participants)

        return self._model_team_to_dto(team)

    def update(self, dto: TeamDTO) -> TeamDTO:
        team = Team.objects.get(id=dto.id)
        team.name = dto.name
        team.participants.set(dto.participants)
        team.save()

        return self._model_team_to_dto(team)

    def delete(self, team_id: int):
        team = Team.objects.get(id=team_id)
        team.delete()
