from typing import Optional, Tuple

from src.domain.base import BaseService
from src.domain.project import FeaturesEntity, ProjectEntity

from .dtos import (
    CommentDTO,
    CreateFeaturesDTO,
    CreateTaskDTO,
    ProjectDTO,
    StatusObject,
    TaskDTO,
    FeaturesDTO,
)
from .entity import TaskEntity, CommentEntity
from .repository import (
    IFeaturesRepository,
    IProjectRepository,
    ITaskRepository,
    ICommentRepository,
)


class ProjectService(BaseService):
    """
    Сервис для работы с проектами.
    """

    def __init__(self, project_repository: IProjectRepository):
        """
        Инициализирует сервис с указанным репозиторием.

        :param project_repository: Репозиторий для работы с проектами.
        """
        self._repository = project_repository

    def get_project_by_slug(self, slug: str) -> ProjectDTO:
        """
        Получает проект по его slug.

        :param slug: Уникальный идентификатор проекта.
        :return: DTO проекта.
        """
        return self._repository.get_project_by_slug(slug)

    def create(
        self, dto: ProjectDTO, user_id: int
    ) -> Tuple[Optional[ProjectDTO], Optional[str]]:
        """
        Создает новый проект.

        :param dto: DTO проекта.
        :param user_id: Идентификатор пользователя.
        :return: Кортеж (DTO проекта, ошибка), где DTO — созданный проект, а ошибка — сообщение об ошибке.
        """
        entity = ProjectEntity(
            name=dto.name,
            logo=dto.logo,
            description=dto.description,
            status=dto.status,
            responsible_id=dto.responsible_id,
            participants=dto.participants,
            date_created=dto.date_created,
        )
        return self.validate_and_save(entity, self._repository, dto, user_id)

    def update(
        self, pk: int, dto: ProjectDTO, user_id: int
    ) -> Tuple[Optional[ProjectDTO], Optional[str]]:
        """
        Обновляет существующий проект.

        :param pk: Идентификатор проекта.
        :param dto: DTO проекта с обновленными данными.
        :param user_id: Идентификатор пользователя.
        :return: Кортеж (DTO проекта, ошибка), где DTO — обновленный проект, а ошибка — сообщение об ошибке.
        """
        entity = ProjectEntity(
            name=dto.name,
            logo=dto.logo,
            description=dto.description,
            status=dto.status,
            responsible_id=dto.responsible_id,
            participants=dto.participants,
            date_created=dto.date_created,
        )
        return self.validate_and_update(
            entity, self._repository, dto, pk, user_id
        )

    def get_project_status_choices(self) -> list[tuple]:
        """
        Возвращает доступные статусы проекта.

        :return: Список кортежей (статус, статус).
        """
        return StatusObject.choices()

    def search_projects(self, query: str) -> list[ProjectDTO]:
        """
        Ищет проекты по запросу.

        :param query: Поисковый запрос.
        :return: Список DTO проектов.
        """
        return self._repository.search_projects(query)
    
    def get_list_participants(self, user_id: id):
        return self._repository.get_list_participants(user_id)


class FeatureService(BaseService):
    """
    Сервис для работы с фичами.
    """

    def __init__(self, features_repository: IFeaturesRepository):
        """
        Инициализирует сервис с указанным репозиторием.

        :param features_repository: Репозиторий для работы с фичами.
        """
        self._repository = features_repository

    def get_features_tags_list(self) -> list[str]:
        """
        Получает список тегов для фич.

        :return: Список тегов.
        """
        return self._repository.get_features_tags_list()

    def get_features_status_list(self) -> list[str]:
        """
        Получает список статусов фич.

        :return: Список статусов.
        """
        return self._repository.get_features_status_list()

    def get_feature_project_list(self) -> list[int]:
        """
        Получает список проектов, связанных с фичами.

        :return: Список идентификаторов проектов.
        """
        return self._repository.get_feature_project_list()

    def create(
        self, dto: CreateFeaturesDTO, user_id: int
    ) -> Tuple[Optional[CreateFeaturesDTO], Optional[str]]:
        """
        Создает новую фичу.

        :param dto: DTO фичи.
        :param user_id: Идентификатор пользователя.
        :return: Кортеж (DTO фичи, ошибка), где DTO — созданная фича, а ошибка — сообщение об ошибке.
        """
        entity = FeaturesEntity(
            name=dto.name,
            importance=dto.importance,
            description=dto.description,
            tags=dto.tags,
            participants=dto.participants,
            responsible_id=dto.responsible_id,
            project_id=dto.project_id,
            status=dto.status,
        )
        return self.validate_and_save(entity, self._repository, dto, user_id)

    def update(
        self, pk: int, dto: CreateFeaturesDTO, user_id: int
    ) -> Tuple[Optional[CreateFeaturesDTO], Optional[str]]:
        """
        Обновляет существующую фичу.

        :param pk: Идентификатор фичи.
        :param dto: DTO фичи с обновленными данными.
        :param user_id: Идентификатор пользователя.
        :return: Кортеж (DTO фичи, ошибка), где DTO — обновленная фича, а ошибка — сообщение об ошибке.
        """
        entity = FeaturesEntity(
            name=dto.name,
            importance=dto.importance,
            description=dto.description,
            tags=dto.tags,
            participants=dto.participants,
            responsible_id=dto.responsible_id,
            project_id=dto.project_id,
            status=dto.status,
        )
        return self.validate_and_update(
            entity, self._repository, dto, pk, user_id
        )

    def get_search_features(self, query: str) -> list[CreateFeaturesDTO]:
        """
        Ищет фичи по запросу.

        :param query: Поисковый запрос.
        :return: Список DTO фич.
        """
        return self._repository.get_search_features(query)


class TaskService(BaseService):
    """
    Сервис для работы с задачами.
    """

    def __init__(self, task_repository: ITaskRepository):
        """
        Инициализирует сервис с указанным репозиторием.

        :param task_repository: Репозиторий для работы с задачами.
        """
        self._repository = task_repository

    def create(
        self, dto: CreateTaskDTO, user_id: int
    ) -> Tuple[Optional[TaskDTO], Optional[str]]:
        """
        Создает новую задачу.

        :param dto: DTO задачи.
        :param user_id: Идентификатор пользователя.
        :return: Кортеж (DTO задачи, ошибка), где DTO — созданная задача, а ошибка — сообщение об ошибке.
        """
        entity = TaskEntity(
            name=dto.name,
            priority=dto.priority,
            contributor_id=dto.contributor_id,
            responsible_id=dto.responsible_id,
            status=dto.status,
            closed_at=dto.closed_at,
            feature_id=dto.feature_id,
            description=dto.description,
            tags=dto.tags,
        )
        return self.validate_and_save(entity, self._repository, dto, user_id)

    def update(
        self, pk: int, dto: TaskDTO, user_id: int
    ) -> Tuple[Optional[TaskDTO], Optional[str]]:
        """
        Обновляет существующую задачу.

        :param pk: Идентификатор задачи.
        :param dto: DTO задачи с обновленными данными.
        :param user_id: Идентификатор пользователя.
        :return: Кортеж (DTO задачи, ошибка), где DTO — обновленная задача, а ошибка — сообщение об ошибке.
        """
        entity = TaskEntity(
            name=dto.name,
            priority=dto.priority,
            contributor_id=dto.contributor_id,
            responsible_id=dto.responsible_id,
            status=dto.status,
            closed_at=dto.closed_at,
            feature_id=dto.feature_id,
            description=dto.description,
            tags=dto.tags,
        )
        return self.validate_and_update(
            entity, self._repository, dto, pk, user_id
        )

    def get_task_status_choices(self) -> list[tuple]:
        """
        Возвращает доступные статусы задачи.

        :return: Список кортежей (статус, статус).
        """
        return self._repository.get_task_status_choices()

    def get_tags_list(self, task_id: int):
        """
        Получает список тегов для задачи.

        :param task_id: Идентификатор задачи.
        :return: Список DTO тегов.
        """
        return self._repository.get_tags_list(task_id)

    def get_tags_id_list(self, tags_id: int) -> list[int]:
        """
        Получает список идентификаторов тегов.

        :param tags_id: Идентификатор тега.
        :return: Список идентификаторов тегов.
        """
        return self._repository.get_tags_id_list(tags_id)

    def get_task_id_list(self, dto: FeaturesDTO) -> list[TaskDTO]:
        """
        Получает список идентификаторов задач для фичи.

        :param dto: DTO фичи.
        :return: Список идентификаторов задач.
        """
        return self._repository.get_task_id_list(dto)

    def create_comment(self, dto: CommentDTO) -> CommentDTO:
        """
        Создает комментарий к задаче.

        :param dto: DTO комментария.
        :return: Созданный DTO комментария.
        """
        return self._repository.create_comment(dto)

    def get_feature_id(self, feature_id: int) -> int:
        """
        Получает идентификатор фичи.

        :param feature_id: Идентификатор фичи.
        :return: Идентификатор фичи.
        """
        return self._repository.get_feature_id(feature_id)
    
    def get_list_responsible(self, user_id: int):
        return self._repository.get_list_responsible(user_id)
    
    def get_list_contributor(self, user_id: int):
        return self._repository.get_list_contributor(user_id)


class CommentService(BaseService):
    """
    Сервис для работы с комментарими.
    """

    def __init__(self, comment_repository: ICommentRepository):
        """
        Инициализирует сервис с указанным репозиторием.

        :param task_repository: Репозиторий для работы с задачами.
        """
        self._repository = comment_repository

    def create(
        self, dto: CommentDTO, user_id: int
    ) -> Tuple[Optional[CommentDTO], Optional[str]]:
        """
        Создает новую задачу.

        :param dto: DTO задачи.
        :param user_id: Идентификатор пользователя.
        :return: Кортеж (DTO задачи, ошибка), где DTO — созданная задача, а ошибка — сообщение об ошибке.
        """
        entity = CommentEntity(
            user_id=dto.user_id,
            comment=dto.comment,
            task_id=dto.task_id,
        )
        return self.validate_and_save(entity, self._repository, dto, user_id)
    
    def update(
        self, pk: int, dto: CommentDTO, user_id: int
    ) -> Tuple[Optional[CommentDTO], Optional[str]]:
        """
        Обновляет существующую задачу.

        :param pk: Идентификатор комментария.
        :param dto: DTO комментария с обновленными данными.
        :param user_id: Идентификатор пользователя.
        :return: Кортеж (DTO задачи, ошибка), где DTO — обновленная задача, а ошибка — сообщение об ошибке.
        """
        entity = CommentEntity(
            user_id=dto.user_id,
            comment=dto.comment,
            task_id=dto.task_id,
        )
        return self.validate_and_update(
            entity, self._repository, dto, pk, user_id
        )
    
    def get_comments_list(self, task_id: int):
        return self._repository.get_comments_list(task_id)