from typing import Any, Callable, Optional, Tuple

from .entity import Entity
from .repository import BaseRepository


class BaseService:
    """
    Базовый класс для сервисов, предоставляющий методы для валидации и обработки данных.
    """

    def __init__(self, repository: BaseRepository):
        """
        Инициализирует сервис с указанным репозиторием.

        :param repository: Репозиторий для работы с данными.
        """
        self._repository = repository

    @classmethod
    def validate_and_process(
        cls,
        entity: Entity,
        repository: BaseRepository,
        dto: Any,
        save_method: Callable[[Any], Any],
    ) -> Tuple[Optional[Any], Optional[str]]:
        """
        Универсальный метод для валидации и сохранения/обновления данных.

        :param entity: Сущность для валидации данных.
        :param repository: Репозиторий для выполнения операций с базой.
        :param dto: DTO с данными.
        :param save_method: Метод репозитория (например, create или update).
        :return: Кортеж (результат операции, ошибка), где результат — результат операции, а ошибка — сообщение об ошибке.
        """
        err = entity.verify_data(dto)
        if err:
            return None, err

        result = save_method(dto)
        return result, None

    @classmethod
    def validate_and_save(
        cls,
        entity: Entity,
        repository: BaseRepository,
        dto: Any,
        user_id: int,
    ) -> Tuple[Optional[Any], Optional[str]]:
        """
        Упрощённая обёртка для создания объектов.

        :param entity: Сущность для валидации данных.
        :param repository: Репозиторий для выполнения операций с базой.
        :param dto: DTO с данными.
        :param user_id: Идентификатор пользователя.
        :return: Кортеж (результат операции, ошибка), где результат — результат операции, а ошибка — сообщение об ошибке.
        """
        # Проверяем наличие прав
        if not repository.has_permission(user_id, 3):
            return None, "У вас нет прав на создание данного объекта"
        return cls.validate_and_process(
            entity, repository, dto, repository.create
        )

    @classmethod
    def validate_and_update(
        cls,
        entity: Entity,
        repository: BaseRepository,
        dto: Any,
        pk: int,
        user_id: int,
    ) -> Tuple[Optional[Any], Optional[str]]:
        """
        Метод для обновления объектов.

        :param entity: Сущность для валидации данных.
        :param repository: Репозиторий для выполнения операций с базой.
        :param dto: DTO с данными.
        :param pk: Первичный ключ объекта.
        :param user_id: Идентификатор пользователя.
        :return: Кортеж (результат операции, ошибка), где результат — результат операции, а ошибка — сообщение об ошибке.
        """
        # Проверяем существование объекта
        if not repository.exists(pk):
            return None, f"Объект с id {pk} не найден."

        # Проверяем наличие прав
        model = repository.get_by_id(pk)
        if not repository.has_permission(user_id, 3, model):
            return None, "У вас нет прав на редактирование данного объекта"

        return cls.validate_and_process(
            entity, repository, dto, lambda d: repository.update(pk, d)
        )

    def exists(self, pk: int) -> bool:
        """
        Проверяет существование объекта по его идентификатору.

        :param pk: Идентификатор объекта.
        :return: True, если объект существует, иначе False.
        """
        return self._repository.exists(pk)

    def get_list(self) -> list[Any]:
        """
        Получает список всех объектов.

        :return: Список объектов.
        """
        return self._repository.get_list()

    def get_by_id(
        self, pk: int, user_id: int
    ) -> Tuple[Optional[Any], Optional[str]]:
        """
        Получает объект по его идентификатору с проверкой прав доступа.

        :param pk: Идентификатор объекта.
        :param user_id: Идентификатор пользователя.
        :return: Кортеж (объект, ошибка), где объект — найденный объект, а ошибка — сообщение об ошибке.
        """
        if not self._repository.exists(pk):
            return None, f"Объект с id {pk} не найден."

        model = self._repository.get_by_id(pk)

        # Проверяем наличие прав на чтение объекта
        if not self._repository.has_permission(user_id, 1, model):
            return None, "У вас нет прав на просмотр данного объекта"

        return model, None

    def delete(self, pk: int, user_id: int) -> Optional[str]:
        """
        Удаляет объект по его идентификатору с проверкой прав доступа.

        :param pk: Идентификатор объекта.
        :param user_id: Идентификатор пользователя.
        :return: Сообщение об ошибке, если удаление не удалось, иначе None.
        """
        model = self._repository.get_by_id(pk)
        if not self._repository.has_permission(user_id, 3, model):
            return "У вас нет прав на удаление данного объекта"
        self._repository.delete(pk)
        return None

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
        return self._repository.has_permission(user_id, action, obj)
