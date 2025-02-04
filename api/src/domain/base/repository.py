from abc import ABC, abstractmethod


class BaseRepository(ABC):
    """
    Базовый репозиторий
    """

    @abstractmethod
    def get_by_id(self, pk: int):
        raise NotImplementedError

    @abstractmethod
    def get_list(self):
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
