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
        """
        Удаляет объект по его идентификатору.

        :param pk: Идентификатор объекта.
        """
        raise NotImplementedError

    @abstractmethod
    def exists(self, pk: int) -> bool:
        """
        Проверяет существование объекта по его идентификатору.

        :param pk: Идентификатор объекта.
        :return: True, если объект существует, иначе False.
        """
        raise NotImplementedError

    @abstractmethod
    def has_permission(
        self, user_id: int, action: int, obj: Optional[Any] = None
    ) -> bool:
        """
        Проверяет наличие прав у пользователя на выполнение действия над объектом.

        :param user_id: Идентификатор пользователя.
        :param action: Код действия.
        :param obj: Объект, над которым выполняется действие. Если None, проверяется глобальное разрешение.
        :return: True, если пользователь имеет права, иначе False.
        """
        raise NotImplementedError
