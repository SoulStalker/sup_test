import abc

from .dtos import CreateTaskDTO, FeaturesDTO, ProjectDTO


class IProjectRepository(abc.ABC):
    @abc.abstractmethod
    def create_project(self, dto: ProjectDTO) -> ProjectDTO:
        raise NotImplementedError

    @abc.abstractmethod
    def update_project(self, project_id: int, dto: ProjectDTO) -> ProjectDTO:
        raise NotImplementedError

    @abc.abstractmethod
    def delete_project(self, project_id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def get_project_list(self) -> list[ProjectDTO]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_project_by_slug(self, slug: str) -> ProjectDTO:
        raise NotImplementedError

    @abc.abstractmethod
    def get_project_by_id(self, project_id: int) -> ProjectDTO:
        raise NotImplementedError

    @abc.abstractmethod
    def get_valid_statuses(self) -> list:
        """Возвращает все допустимые статусы."""
        raise NotImplementedError

    @abc.abstractmethod
    def status_orm_to_dto(self, status: str) -> str:
        """Преобразует статус в DTO."""
        raise NotImplementedError

    def search_projects(self, query: str) -> list[ProjectDTO]:
        raise NotImplementedError


class IFeaturesRepository(abc.ABC):
    @abc.abstractmethod
    def get_features_list(self) -> list[FeaturesDTO]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_features_tags_list(self, feature_id: int) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_features_status_list(self) -> list:
        raise NotImplementedError

    @abc.abstractmethod
    def get_feature_project_list(self) -> list:
        raise NotImplementedError

    @abc.abstractmethod
    def create_feature(self, dto: FeaturesDTO) -> FeaturesDTO:
        raise NotImplementedError

    def get_feature_by_id(self, feature_id: int) -> FeaturesDTO:
        raise NotImplementedError

    def update_features(
        self, feature_id: int, dto: FeaturesDTO
    ) -> FeaturesDTO:
        raise NotImplementedError

    def delete_features(self, feature_id: int):
        raise NotImplementedError

    def get_search_features(self, query: str) -> list[FeaturesDTO]:
        raise NotImplementedError


class ITaskRepository(abc.ABC):
    @abc.abstractmethod
    def get_tasks_list(self) -> list:
        raise NotImplementedError

    @abc.abstractmethod
    def create_task(self, dto: CreateTaskDTO):
        raise NotImplementedError

    @abc.abstractmethod
    def get_task_by_id(self, task_id: int) -> FeaturesDTO:
        raise NotImplementedError

    @abc.abstractmethod
    def update_task(self, task_id: int, dto: FeaturesDTO) -> FeaturesDTO:
        raise NotImplementedError

    @abc.abstractmethod
    def delete_task(self, task_id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def get_task_status_choices(self) -> list:
        raise NotImplementedError
