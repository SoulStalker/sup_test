"""
Работа с базой данных, паттерн "Репозиторий"
Либо можно использовать DAO
преобразует данные в нативные объекты питона и наоборот
пишет в базу и читает из базы
"""

from abc import ABC, abstractmethod

from src.domain.base import BaseRepository

from .dtos import CategoryObject, MeetDTO
from .entity import CategoryEntity


class IMeetRepository(BaseRepository):
    """
    Интерфейс репозитория митов
    """

    @abstractmethod
    def create(self, dto: MeetDTO) -> MeetDTO:
        raise NotImplementedError

    @abstractmethod
    def update(self, meet_id: int, dto: MeetDTO):
        raise NotImplementedError

    @abstractmethod
    def get_meets_by_category(self, category_id: int):
        raise NotImplementedError

    @abstractmethod
    def set_participant_statuses(
        self, participant_statuses: dict, meet_id: int
    ):
        raise NotImplementedError

    def get_participants_statuses(self, meet_id):
        raise NotImplementedError


class ICategoryRepository(ABC):
    """
    Интерфейс репозитория категорий
    """

    @abstractmethod
    def create(self, category: CategoryEntity):
        raise NotImplementedError

    @abstractmethod
    def update(self, category_id: int, dto: CategoryObject):
        raise NotImplementedError
