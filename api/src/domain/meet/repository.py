"""
Работа с базой данных, паттерн "Репозиторий"
Либо можно использовать DAO
преобразует данные в нативные объекты питона и наоборот
пишет в базу и читает из базы
"""

import abc
from .dtos import MeetDTO, CategoryObject


class IMeetRepository(abc.ABC):
    """
    Интерфейс репозитория митов
    """

    @abc.abstractmethod
    def create(self, dto: MeetDTO) -> MeetDTO:
        pass

    @abc.abstractmethod
    def update(self, meet_id: int, dto: MeetDTO):
        pass

    @abc.abstractmethod
    def delete(self, meet_id: int):
        pass

    @abc.abstractmethod
    def get_meet_by_id(self, meet_id: int):
        pass

    @abc.abstractmethod
    def get_meets_list(self):
        pass

    @abc.abstractmethod
    def get_meets_by_category(self, category_id: int):
        pass

    @abc.abstractmethod
    def set_participant_statuses(self, participant_statuses: dict, meet_id: int):
        pass

    def get_participants_statuses(self, meet_id):
        pass


class ICategoryRepository(abc.ABC):
    """
    Интерфейс репозитория категорий
    """

    @abc.abstractmethod
    def create(self, category_name: str):
        pass

    @abc.abstractmethod
    def update(self, category_id: int, dto: CategoryObject):
        pass

    @abc.abstractmethod
    def delete(self, category_id: int):
        pass

    @abc.abstractmethod
    def get_categories_list(self):
        pass

    @abc.abstractmethod
    def get_category_by_id(self, category_id: int):
        pass
