from src.domain.authorization import AuthorizationService
from src.domain.base import BaseService

from .dtos import CategoryObject, MeetDTO
from .entity import CategoryEntity, MeetEntity
from .repository import ICategoryRepository, IMeetRepository


class MeetService(BaseService):
    def __init__(
        self,
        repository: IMeetRepository,
        category_repository: ICategoryRepository,
        authorization_service: AuthorizationService = AuthorizationService,
    ):
        self._repository = repository
        self.__category_repository = category_repository
        self._authorization_service = authorization_service

    def create(self, dto, user_id):
        """
        Создание мита с проверкой прав пользователя.
        """
        if not self._authorization_service.can_create_meet(user_id):
            raise PermissionError(
                "User does not have permission to create meets"
            )

        entity = MeetEntity(
            dto.category_id,
            dto.title,
            dto.start_time,
            dto.author_id,
            dto.responsible_id,
            dto.participant_statuses,
        )
        return self.validate_and_save(entity, self._repository, dto)

    def update(self, pk, dto, user_id):
        """
        Обновление мита с проверкой прав пользователя.
        """
        if not self._authorization_service.can_create_meet(self, user_id):
            print("User does not have permission to update meets")
            raise PermissionError(
                "User does not have permission to update meets"
            )
        entity = MeetEntity(
            category_id=dto.category_id,
            title=dto.title,
            start_time=dto.start_time,
            author_id=dto.author_id,
            responsible_id=dto.responsible_id,
            participant_statuses=dto.participant_statuses,
        )
        return self.validate_and_update(entity, self._repository, dto, pk)

    def get_meets_by_category(self, dto, user_id) -> list[MeetDTO]:
        """
        Получение митов по категории с проверкой прав пользователя.
        """
        if not self._authorization_service.can_view_meet(user_id):
            raise PermissionError(
                "User does not have permission to view meets"
            )

        return self._repository.get_meets_by_category(dto)

    def get_participants_statuses(self, meet_id: int):
        return self._repository.get_participants_statuses(meet_id)

    def set_participants_statuses(self, participant_statuses, meet_id: int):
        return self._repository.set_participant_statuses(
            participant_statuses, meet_id
        )


class MeetCategoryService(BaseService):
    def __init__(
        self,
        repository: ICategoryRepository,
    ):
        self._repository = repository

    def create(self, category_name):
        """
        Создание категории
        """

        entity = CategoryEntity(name=category_name)
        dto = CategoryEntity(name=category_name)

        return self.validate_and_save(entity, self._repository, dto)

    def update(self, pk, category_name):
        """
        Обновление категории
        """
        entity = CategoryEntity(name=category_name)
        dto = CategoryObject(name=category_name)
        return self.validate_and_update(entity, self._repository, dto, pk)
