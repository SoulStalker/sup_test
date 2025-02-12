from abc import abstractmethod
from typing import Optional, Tuple

from src.domain.base import BaseRepository

from .dtos import CreateTeamDTO, TeamDTO


class ITeamRepository(BaseRepository):
    """
    Интерфейс репозитория для работы с командами.
    """

    @abstractmethod
    def create(
        self, dto: CreateTeamDTO
    ) -> Tuple[Optional[TeamDTO], Optional[str]]:
        """
        Создает новую команду.

        :param dto: DTO команды.
        :return: Кортеж (DTO команды, ошибка), где DTO — созданная команда, а ошибка — сообщение об ошибке.
        """
        raise NotImplementedError

    @abstractmethod
    def update(
        self, pk: int, dto: TeamDTO
    ) -> Tuple[Optional[TeamDTO], Optional[str]]:
        """
        Обновляет данные команды.

        :param pk: Идентификатор команды.
        :param dto: DTO команды с обновленными данными.
        :return: Кортеж (DTO команды, ошибка), где DTO — обновленная команда, а ошибка — сообщение об ошибке.
        """
        raise NotImplementedError
