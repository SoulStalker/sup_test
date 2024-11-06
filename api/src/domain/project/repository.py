from .dtos import ProjectDTO, FeaturesDTO
import abc

class IProjectRepository(abc.ABC):
    @abc.abstractmethod
    def create_project(self, dto: ProjectDTO) -> ProjectDTO:
        pass

    @abc.abstractmethod
    def update_project(self, project_id: int, dto: ProjectDTO) -> ProjectDTO:
        pass

    @abc.abstractmethod
    def delete_project(self, project_id: int):
        pass

    @abc.abstractmethod
    def get_project_list(self) -> list[ProjectDTO]:
        pass

    @abc.abstractmethod
    def get_project_by_slug(self, slug: str) -> ProjectDTO:
        pass

    @abc.abstractmethod
    def get_project_by_id(self, project_id: int) -> ProjectDTO:
        pass

    @abc.abstractmethod
    def get_valid_statuses(self) -> list:
        """Возвращает все допустимые статусы."""
        pass

    @abc.abstractmethod
    def status_orm_to_dto(self, status: str) -> str:
        """Преобразует статус в DTO."""
        pass

    def search_projects(self, query: str) -> list[ProjectDTO]:
        pass


class IFeaturesRepository(abc.ABC):
    @abc.abstractmethod
    def get_features_list(self) -> list[FeaturesDTO]:
        pass

    @abc.abstractmethod
    def get_features_tags_list(self, feature_id: int) -> list[str]:
        pass

    @abc.abstractmethod
    def get_features_status_list(self) -> list:
        pass

    @abc.abstractmethod
    def get_feature_project_list(self) -> list:
        pass

    @abc.abstractmethod
    def create_feature(self, dto: FeaturesDTO) -> FeaturesDTO:
        pass

    def get_feature_by_id(self, feature_id: int) -> FeaturesDTO:
        pass

    def update_features(self, feature_id: int, dto: FeaturesDTO) -> FeaturesDTO:
        pass