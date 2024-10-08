"""
Работа с базой данных, паттерн "Репозиторий"
Либо можно использовать DAO
преобразует данные в нативные объекты питона и наоборот
пишет в базу и читает из базы
"""
import abc
from src.models.meets import Category


class IMeetRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, meet):
        pass

    def delete(self, meet):
        pass

    def get_list(self, meet):
        pass


class ICategoryRepository:
    model = Category

    def create(self, category):
        pass

    def delete(self, category):
        pass

    def get_list(self) -> list[Category]:
        pass
