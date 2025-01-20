from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from src.domain.teams import ITeamRepository
from src.domain.teams.dtos import CreateTeamDTO, TeamDTO
from src.models.models import Team

user = get_user_model()


class TeamRepository(ITeamRepository):
    model = Team

    @classmethod
    def _model_team_to_dto(cls, team) -> TeamDTO:
        return TeamDTO(
            id=team.id,
            name=team.name,
            participants=[
                participant.id for participant in team.participants.all()
            ],
        )

    def exists(self, pk: int) -> bool:
        return Team.objects.filter(id=pk).exists()

    def get_list(self) -> list[TeamDTO]:
        teams = Team.objects.all()
        return [
            TeamDTO(id=team.id, name=team.name, participants=team.participants)
            for team in teams
        ]

    def get_by_id(self, team_id: int) -> TeamDTO:
        team = Team.objects.get(id=team_id)
        return self._model_team_to_dto(team)

    def create(self, dto: CreateTeamDTO) -> tuple[None, Any] | TeamDTO:
        team = Team(name=dto.name)
        team.save()
        team.participants.set(dto.participants)

        return self._model_team_to_dto(team)

    def update(self, pk: int, dto: TeamDTO) -> TeamDTO:
        team = Team.objects.get(id=pk)
        team.name = dto.name
        team.participants.set(dto.participants)
        team.save()

        return self._model_team_to_dto(team)

    def delete(self, pk: int):
        team = Team.objects.get(id=pk)
        team.delete()

    def has_permission(self, user_id: int, action: str, obj=None) -> bool:
        """
        Проверка наличия прав у пользователя на выполнение действия.
        :param user_id: ID пользователя
        :param action: код действия (например, "EDIT", "READ", "COMMENT")
        :param obj: объект, для которого проверяются права (например, Meet)
        :return: bool
        """
        content_type = ContentType.objects.get_for_model(self.model)
        # для митов будем считать то нам не надо распределять права по митам
        # поэтому object_id = None
        # object_id = obj.id if obj else None
        object_id = None

        current_user = get_object_or_404(user, pk=user_id)
        permission = current_user.permissions.filter(
            code=action,
            content_type=content_type,
            object_id=object_id,
        ).exists()
        return permission
