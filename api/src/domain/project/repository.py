from abc import abstractmethod

from src.domain.base import BaseRepository

from .dtos import CreateTaskDTO, FeaturesDTO, ProjectDTO, TagDTO, TaskDTO


class IProjectRepository(BaseRepository):
    @abstractmethod
    def create(self, dto: ProjectDTO) -> ProjectDTO:
        raise NotImplementedError

    @abstractmethod
    def update_project(self, project_id: int, dto: ProjectDTO) -> ProjectDTO:
        raise NotImplementedError

    @abstractmethod
    def get_project_by_slug(self, slug: str) -> ProjectDTO:
        raise NotImplementedError

    @abstractmethod
    def get_valid_statuses(self) -> list:
        """Возвращает все допустимые статусы."""
        raise NotImplementedError

    @abstractmethod
    def status_orm_to_dto(self, status: str) -> str:
        """Преобразует статус в DTO."""
        raise NotImplementedError

    def search_projects(self, query: str) -> list[ProjectDTO]:
        raise NotImplementedError


class IFeaturesRepository(BaseRepository):

    @abstractmethod
    def get_features_tags_list(self, feature_id: int) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def get_features_status_list(self) -> list:
        raise NotImplementedError

    @abstractmethod
    def get_feature_project_list(self) -> list:
        raise NotImplementedError

    @abstractmethod
    def create_feature(self, dto: FeaturesDTO) -> FeaturesDTO:
        raise NotImplementedError

    def update_features(
        self, feature_id: int, dto: FeaturesDTO
    ) -> FeaturesDTO:
        raise NotImplementedError


class ITaskRepository(BaseRepository):

    @abstractmethod
    def create_task(self, dto: CreateTaskDTO):
        raise NotImplementedError

    @abstractmethod
    def update_task(self, dto: TaskDTO) -> TaskDTO:
        raise NotImplementedError

    @abstractmethod
    def get_tags_list(self, task_id: int) -> list[TagDTO]:
        raise NotImplementedError
