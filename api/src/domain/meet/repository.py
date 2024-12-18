"""
Работа с базой данных, паттерн "Репозиторий"
Либо можно использовать DAO
преобразует данные в нативные объекты питона и наоборот
пишет в базу и читает из базы
"""

import abc

from .dtos import CategoryObject, MeetDTO


class BaseRepository(abc.ABC):
    """
    Базовый репозиторий
    """

    @abc.abstractmethod
    def get_by_id(self, pk: int):
        raise NotImplementedError

    @abc.abstractmethod
    def get_list(self):
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, pk: int) -> None:
        raise NotImplementedError


class IMeetRepository(BaseRepository):
    """
    Интерфейс репозитория митов
    """

    @abc.abstractmethod
    def create(self, dto: MeetDTO) -> MeetDTO:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, meet_id: int, dto: MeetDTO):
        raise NotImplementedError

    @abc.abstractmethod
    def get_meets_by_category(self, category_id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def set_participant_statuses(
        self, participant_statuses: dict, meet_id: int
    ):
        raise NotImplementedError

    def get_participants_statuses(self, meet_id):
        raise NotImplementedError


class ICategoryRepository(abc.ABC):
    """
    Интерфейс репозитория категорий
    """

    @abc.abstractmethod
    def create(self, category_name: str):
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, category_id: int, dto: CategoryObject):
        raise NotImplementedError
