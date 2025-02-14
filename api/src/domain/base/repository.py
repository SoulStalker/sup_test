from abc import ABC, abstractmethod
from typing import Any, List, Optional


class BaseRepository(ABC):
    """
    Базовый класс для репозиториев, определяющий интерфейс для работы с данными.
    """

    @abstractmethod
    def get_by_id(self, pk: int) -> Optional[Any]:
        """
        Получает объект по его идентификатору.

        :param pk: Идентификатор объекта.
        :return: Объект или None, если объект не найден.
        """
        raise NotImplementedError

    @abstractmethod
    def get_list(self) -> List[Any]:
        """
        Получает список всех объектов.

        :return: Список объектов.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, pk: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def exists(self, pk: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def has_permission(self, user_id: int, action: int, obj=None) -> bool:
        raise NotImplementedError
