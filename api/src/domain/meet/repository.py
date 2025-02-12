from abc import ABC, abstractmethod
from typing import Dict, List

from src.domain.base import BaseRepository

from .dtos import CategoryObject, MeetDTO
from .entity import CategoryEntity


class IMeetRepository(BaseRepository):
    """
    Интерфейс репозитория для работы с митами.
    """

    @abstractmethod
    def create(self, dto: MeetDTO) -> MeetDTO:
        """
        Создает новый мит.

        :param dto: DTO мита.
        :return: Созданный DTO мита.
        """
        raise NotImplementedError

    @abstractmethod
    def update(self, meet_id: int, dto: MeetDTO) -> None:
        """
        Обновляет данные мита.

        :param meet_id: Идентификатор мита.
        :param dto: DTO мита с обновленными данными.
        """
        raise NotImplementedError

    @abstractmethod
    def get_meets_by_category(self, category_id: int) -> List[MeetDTO]:
        """
        Получает список митов по категории.

        :param category_id: Идентификатор категории.
        :return: Список DTO митов.
        """
        raise NotImplementedError

    @abstractmethod
    def set_participant_statuses(
        self, participant_statuses: Dict[int, str], meet_id: int
    ) -> None:
        """
        Устанавливает статусы участников мита.

        :param participant_statuses: Словарь статусов участников.
        :param meet_id: Идентификатор мита.
        """
        raise NotImplementedError

    @abstractmethod
    def get_participants_statuses(self, meet_id: int) -> Dict[int, str]:
        """
        Получает статусы участников мита.

        :param meet_id: Идентификатор мита.
        :return: Словарь статусов участников.
        """
        raise NotImplementedError


class ICategoryRepository(ABC):
    """
    Интерфейс репозитория для работы с категориями.
    """

    @abstractmethod
    def create(self, category: CategoryEntity, user_id: int) -> CategoryObject:
        """
        Создает новую категорию.

        :param category: Сущность категории.
        :param user_id: Идентификатор пользователя.
        :return: Созданный объект категории.
        """
        raise NotImplementedError

    @abstractmethod
    def update(self, category_id: int, dto: CategoryObject) -> None:
        """
        Обновляет данные категории.

        :param category_id: Идентификатор категории.
        :param dto: Объект категории с обновленными данными.
        """
        raise NotImplementedError
