"""
Работа с базой данных, паттерн "Репозиторий"
Либо можно использовать DAO
преобразует данные в нативные объекты питона и наоборот
пишет в базу и читает из базы
"""
import abc


class IMeetRepository(abc.ABC):
    @abc.abstractmethod
    # что должен принимать данный метод? ДТО?
    def create(self, meet):
        pass

    @abc.abstractmethod
    def update(self, meet_id: int):
        pass

    @abc.abstractmethod
    def delete(self, meet_id: int):
        pass

    @abc.abstractmethod
    def get_meets_list(self):
        pass

    @abc.abstractmethod
    def get_meet_by_id(self, meet_id: int):
        pass

    @abc.abstractmethod
    def get_meets_by_category(self, category_id: int):
        pass


class ICategoryRepository(abc.ABC):
    # Может использовать один интерфейс для мита и категории и расширить метод уже в экземпляре?
    @abc.abstractmethod
    # что должен принимать данный метод? может строку так как очень простой?
    def create(self, category_name: str):
        pass

    @abc.abstractmethod
    def update(self, category_id: int):
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
