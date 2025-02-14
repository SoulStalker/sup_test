from typing import Optional, Tuple

from src.domain.base import BaseService

from .dtos import CreateTeamDTO, TeamDTO
from .repository import ITeamRepository


class TeamService(BaseService):
    """
    Сервис для работы с командами.
    """

    def __init__(self, repository: ITeamRepository):
        """
        Инициализирует сервис с указанным репозиторием.

        :param repository: Репозиторий для работы с командами.
        """
        self._repository = repository

    def create(
        self, dto: CreateTeamDTO, user_id: int
    ) -> Tuple[Optional[TeamDTO], Optional[str]]:
        """
        Создает новую команду.

        :param dto: DTO команды.
        :param user_id: Идентификатор пользователя.
        :return: Кортеж (DTO команды, ошибка), где DTO — созданная команда, а ошибка — сообщение об ошибке.
        """
        entity = CreateTeamDTO(name=dto.name, participants=dto.participants)
        return self.validate_and_save(entity, self._repository, dto, user_id)

    def update(
        self, pk: int, dto: TeamDTO, user_id: int
    ) -> Tuple[Optional[TeamDTO], Optional[str]]:
        """
        Обновляет существующую команду.

        :param pk: Идентификатор команды.
        :param dto: DTO команды с обновленными данными.
        :param user_id: Идентификатор пользователя.
        :return: Кортеж (DTO команды, ошибка), где DTO — обновленная команда, а ошибка — сообщение об ошибке.
        """
        entity = TeamDTO(
            id=dto.id, name=dto.name, participants=dto.participants
        )
        return self.validate_and_update(
            entity, self._repository, dto, pk, user_id
        )
