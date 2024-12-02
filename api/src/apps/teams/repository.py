from src.domain.teams.dtos import TeamDTO
from src.domain.teams.repository import ITeamRepository
from src.models.models import Team


class TeamRepository(ITeamRepository):

    @classmethod
    def _model_team_to_dto(cls, team) -> TeamDTO:
        return TeamDTO(id=team.id, name=team.name)

    def get_team_list(self) -> list[TeamDTO]:
        teams = Team.objects.all()
        return [TeamDTO(id=team.id, name=team.name) for team in teams]

    def get_team_by_id(self, team_id: int) -> TeamDTO:
        team = Team.objects.get(id=team_id)
        return TeamDTO(id=team.id, name=team.name)

    def create(self, team_name: str) -> TeamDTO:
        team = Team(name=team_name)
        team.save()
        return self._model_team_to_dto(team)

    def update(self, team_id: int, team_name: str) -> TeamDTO:
        team = Team.objects.get(id=team_id)
        team.name = team_name
        team.save()
        return self._model_team_to_dto(team)

    def delete(self, team_id: int):
        team = Team.objects.get(id=team_id)
        team.delete()
