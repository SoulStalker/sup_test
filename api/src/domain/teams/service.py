from typing import Any

from .dtos import CreateTeamDTO, TeamDTO
from .repository import ITeamRepository


class TeamService:
    def __init__(self, repository: ITeamRepository):
        self.__repository = repository

    def get_team_list(self) -> list[TeamDTO]:
        return self.__repository.get_team_list()

    def get_team_by_id(self, team_id: int) -> TeamDTO:
        return self.__repository.get_team_by_id(team_id)

    def create(self, team_name: str) -> tuple[None, Any] | TeamDTO:
        team = CreateTeamDTO(name=team_name)
        err = team.verify_data()
        if err:
            return None, err
        return self.__repository.create(team_name)

    def update(self, team_id: int, team_name: str) -> TeamDTO:
        return self.__repository.update(team_id, team_name)

    def delete(self, team_id: int):
        return self.__repository.delete(team_id)
