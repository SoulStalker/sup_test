from typing import Dict, List, Optional, Tuple

from src.domain.base import BaseService

from .dtos import CategoryObject, MeetDTO
from .entity import CategoryEntity, MeetEntity
from .repository import ICategoryRepository, IMeetRepository


class MeetService(BaseService):
    """
    Сервис для работы с митами.
    """

    def __init__(
        self,
        repository: IMeetRepository,
        category_repository: ICategoryRepository,
    ):
        """
        Инициализирует сервис с указанными репозиториями.

        :param repository: Репозиторий для работы с митами.
        :param category_repository: Репозиторий для работы с категориями.
        """
        self._repository = repository
        self.__category_repository = category_repository

    def create(
        self, dto: MeetDTO, user_id: int
    ) -> Tuple[Optional[MeetDTO], Optional[str]]:
        """
        Создает новый мит с проверкой прав пользователя.

        :param dto: DTO мита.
        :param user_id: Идентификатор пользователя.
        :return: Кортеж (DTO мита, ошибка), где DTO — созданный мит, а ошибка — сообщение об ошибке.
        """
        entity = MeetEntity(
            dto.category_id,
            dto.title,
            dto.start_time,
            dto.author_id,
            dto.responsible_id,
            dto.participant_statuses,
        )
        return self.validate_and_save(entity, self._repository, dto, user_id)

    def update(
        self, pk: int, dto: MeetDTO, user_id: int
    ) -> Tuple[Optional[MeetDTO], Optional[str]]:
        """
        Обновляет мит с проверкой прав пользователя.

        :param pk: Идентификатор мита.
        :param dto: DTO мита с обновленными данными.
        :param user_id: Идентификатор пользователя.
        :return: Кортеж (DTO мита, ошибка), где DTO — обновленный мит, а ошибка — сообщение об ошибке.
        """
        entity = MeetEntity(
            category_id=dto.category_id,
            title=dto.title,
            start_time=dto.start_time,
            author_id=dto.author_id,
            responsible_id=dto.responsible_id,
            participant_statuses=dto.participant_statuses,
        )
        return self.validate_and_update(
            entity, self._repository, dto, pk, user_id
        )

    def get_meets_by_category(self, category_id: int) -> List[MeetDTO]:
        """
        Получает список митов по категории.

        :param category_id: Идентификатор категории.
        :return: Список DTO митов.
        """
        return self._repository.get_meets_by_category(category_id)

    def get_participants_statuses(self, meet_id: int) -> Dict[int, str]:
        """
        Получает статусы участников мита.

        :param meet_id: Идентификатор мита.
        :return: Словарь статусов участников.
        """
        return self._repository.get_participants_statuses(meet_id)

    def set_participants_statuses(
        self, participant_statuses: Dict[int, str], meet_id: int
    ) -> None:
        """
        Устанавливает статусы участников мита.

        :param participant_statuses: Словарь статусов участников.
        :param meet_id: Идентификатор мита.
        """
        self._repository.set_participant_statuses(
            participant_statuses, meet_id
        )


class MeetCategoryService(BaseService):
    """
    Сервис для работы с категориями митов.
    """

    def __init__(
        self,
        repository: ICategoryRepository,
    ):
        """
        Инициализирует сервис с указанным репозиторием.

        :param repository: Репозиторий для работы с категориями.
        """
        self._repository = repository

    def create(
        self, category_name: str, user_id: int
    ) -> Tuple[Optional[CategoryObject], Optional[str]]:
        """
        Создает новую категорию.

        :param category_name: Название категории.
        :param user_id: Идентификатор пользователя.
        :return: Кортеж (объект категории, ошибка), где объект — созданная категория, а ошибка — сообщение об ошибке.
        """
        entity = CategoryEntity(name=category_name)
        dto = CategoryObject(
            pk=0, name=category_name
        )  # pk будет установлен при создании
        return self.validate_and_save(entity, self._repository, dto, user_id)

    def update(
        self, pk: int, category_name: str, user_id: int
    ) -> Tuple[Optional[CategoryObject], Optional[str]]:
        """
        Обновляет категорию.

        :param pk: Идентификатор категории.
        :param category_name: Новое название категории.
        :param user_id: Идентификатор пользователя.
        :return: Кортеж (объект категории, ошибка), где объект — обновленная категория, а ошибка — сообщение об ошибке.
        """
        entity = CategoryEntity(name=category_name)
        dto = CategoryObject(pk=pk, name=category_name)
        return self.validate_and_update(
            entity, self._repository, dto, pk, user_id
        )
