from .repository import IProjectRepository, IFeaturesRepository
from src.domain.project.entity import ProjectEntity, FeaturesEntity
from .dtos import ProjectDTO, StatusObject, FeaturesChoicesObject, FeaturesDTO

class ProjectService:

    def __init__(self, project_repository: IProjectRepository):
        self.__project_repository = project_repository

    def get_project_by_slug(self, slug: str) -> ProjectDTO:
        """Получение проекта по его slug."""
        return self.__project_repository.get_project_by_slug(slug)

    def get_projects_list(self) -> list[ProjectDTO]:
        """Получение списка всех проектов."""
        return self.__project_repository.get_project_list()

    def create_project(self, dto: ProjectDTO):
        """Создание нового проекта."""
        project = ProjectEntity(
            name=dto.name,
            logo=dto.logo,
            description=dto.description,
            status=dto.status,
            responsible_id=dto.responsible_id,
            participants=dto.participants,
            date_created=dto.date_created
        )

        err = project.verify_data()
        if err:
            return err
        return self.__project_repository.create_project(project)

    def update_project(self, project_id, dto):
        """Обновление существующего проекта."""
        return self.__project_repository.update_project(project_id, dto)

    def delete_project(self, project_id: int):
        """Удаление существующего проекта."""
        return self.__project_repository.delete_project(project_id)

    def get_project_status_choices(self):
        """Возвращает доступные статусы проекта."""
        return StatusObject.choices()


    def get_project_by_id(self, project_id: int) -> ProjectDTO:
        """Получение проекта по его id."""
        return self.__project_repository.get_project_by_id(project_id)

    def search_projects(self, query: str):
        return self.__project_repository.search_projects(query)

class FeatureService:
    def __init__(self, features_repository: IFeaturesRepository):
        self.__features_repository = features_repository

    def get_features_list(self) -> list[FeaturesDTO]:
        return self.__features_repository.get_features_list()

    def get_features_tags_list(self) -> list:
        return self.__features_repository.get_features_tags_list()

    def get_features_status_list(self) -> list:
        return self.__features_repository.get_features_status_list()

    def get_feature_project_list(self) -> list:
        return self.__features_repository.get_feature_project_list()

    def create_features(self, dto: FeaturesDTO):
        feature = FeaturesEntity(
            name=dto.name,
            importance=dto.importance,
            description=dto.description,
            tags=dto.tags,
            participants=dto.participants,
            responsible_id=dto.responsible_id,
            project_id=dto.project_id,
            status=dto.status
        )

        err = feature.verify_data()
        if err:
            return err
        return self.__features_repository.create_feature(feature)

    def get_feature_by_id(self, feature_id: int) -> FeaturesDTO:
        return self.__features_repository.get_feature_by_id(feature_id)