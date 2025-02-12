from abc import abstractmethod
from typing import Optional

from src.domain.base import BaseRepository

from .dtos import InviteDTO


class IInviteRepository(BaseRepository):
    """
    Интерфейс репозитория для работы с приглашениями.
    """

    @abstractmethod
    def create(self, user_id: int) -> Optional[InviteDTO]:
        """
        Создает новое приглашение для указанного пользователя.

        :param user_id: Идентификатор пользователя.
        :return: DTO созданного приглашения или None, если создание не удалось.
        """
        raise NotImplementedError

    @abstractmethod
    def update_status(self, invite_id: int, status: str) -> None:
        """
        Обновляет статус приглашения.

        :param invite_id: Идентификатор приглашения.
        :param status: Новый статус приглашения.
        """
        raise NotImplementedError

    @abstractmethod
    def create_invite_dto(self, invitation_code: str) -> Optional[InviteDTO]:
        """
        Создает DTO приглашения на основе кода приглашения.

        :param invitation_code: Код приглашения.
        :return: DTO приглашения или None, если приглашение не найдено.
        """
        raise NotImplementedError
