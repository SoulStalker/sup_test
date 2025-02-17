from abc import abstractmethod

from src.domain.base import BaseRepository

from .dtos import (
    CreateFeaturesDTO,
    CreateTaskDTO,
    ProjectDTO,
    TagDTO,
    TaskDTO,
    CommentDTO,
)


class IProjectRepository(BaseRepository):
    """
    Интерфейс репозитория для работы с проектами.
    """

    @abstractmethod
    def create(self, dto: ProjectDTO) -> ProjectDTO:
        """
        Создает новый проект.

        :param dto: DTO проекта.
        :return: Созданный DTO проекта.
        """
        raise NotImplementedError

    @abstractmethod
    def update(self, project_id: int, dto: ProjectDTO) -> ProjectDTO:
        """
        Обновляет данные проекта.

        :param project_id: Идентификатор проекта.
        :param dto: DTO проекта с обновленными данными.
        :return: Обновленный DTO проекта.
        """
        raise NotImplementedError

    @abstractmethod
    def get_project_by_slug(self, slug: str) -> ProjectDTO:
        """
        Получает проект по его slug.

        :param slug: Уникальный идентификатор проекта.
        :return: DTO проекта.
        """
        raise NotImplementedError

    @abstractmethod
    def get_valid_statuses(self) -> list[str]:
        """
        Возвращает все допустимые статусы проекта.

        :return: Список допустимых статусов.
        """
        raise NotImplementedError

    @abstractmethod
    def status_orm_to_dto(self, status: str) -> str:
        """
        Преобразует статус из ORM в DTO.

        :param status: Статус в формате ORM.
        :return: Статус в формате DTO.
        """
        raise NotImplementedError

    @abstractmethod
    def search_projects(self, query: str) -> list[ProjectDTO]:
        """
        Ищет проекты по запросу.

        :param query: Поисковый запрос.
        :return: Список DTO проектов.
        """
        raise NotImplementedError


class IFeaturesRepository(BaseRepository):
    """
    Интерфейс репозитория для работы с фичами.
    """

    @abstractmethod
    def get_features_tags_list(self, feature_id: int) -> list[str]:
        """
        Получает список тегов для фичи.

        :param feature_id: Идентификатор фичи.
        :return: Список тегов.
        """
        raise NotImplementedError

    @abstractmethod
    def get_features_status_list(self) -> list[str]:
        """
        Получает список статусов фич.

        :return: Список статусов.
        """
        raise NotImplementedError

    @abstractmethod
    def get_feature_project_list(self) -> list[int]:
        """
        Получает список проектов, связанных с фичами.

        :return: Список идентификаторов проектов.
        """
        raise NotImplementedError

    @abstractmethod
    def create(self, dto: CreateFeaturesDTO) -> CreateFeaturesDTO:
        """
        Создает новую фичу.

        :param dto: DTO фичи.
        :return: Созданный DTO фичи.
        """
        raise NotImplementedError

    @abstractmethod
    def update(
        self, feature_id: int, dto: CreateFeaturesDTO
    ) -> CreateFeaturesDTO:
        """
        Обновляет данные фичи.

        :param feature_id: Идентификатор фичи.
        :param dto: DTO фичи с обновленными данными.
        :return: Обновленный DTO фичи.
        """
        raise NotImplementedError


class ITaskRepository(BaseRepository):
    """
    Интерфейс репозитория для работы с задачами.
    """

    @abstractmethod
    def create(self, dto: CreateTaskDTO) -> TaskDTO:
        """
        Создает новую задачу.

        :param dto: DTO задачи.
        :return: Созданный DTO задачи.
        """
        raise NotImplementedError

    @abstractmethod
    def update(self, pk: int, dto: TaskDTO) -> TaskDTO:
        """
        Обновляет данные задачи.

        :param pk: Идентификатор задачи.
        :param dto: DTO задачи с обновленными данными.
        :return: Обновленный DTO задачи.
        """
        raise NotImplementedError

    @abstractmethod
    def get_tags_list(self, task_id: int) -> list[TagDTO]:
        """
        Получает список тегов для задачи.

        :param task_id: Идентификатор задачи.
        :return: Список DTO тегов.
        """
        raise NotImplementedError


class ICommentRepository(BaseRepository):
    """
    Интерфейс репозитория для работы с комментариями.
    """

    @abstractmethod
    def create(self, dto: CommentDTO) -> CommentDTO:
        """
        Создает новый комментарий.

        :param dto: DTO комментария.
        :return: Созданный DTO комментария.
        """
        raise NotImplementedError