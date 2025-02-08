from src.domain.base import BaseService
from src.domain.project import FeaturesEntity, ProjectEntity

from .dtos import (
    CommentDTO,
    CreateFeaturesDTO,
    CreateTaskDTO,
    ProjectDTO,
    StatusObject,
    TaskDTO,
)
from .entity import TaskEntity
from .repository import (
    IFeaturesRepository,
    IProjectRepository,
    ITaskRepository,
)


class ProjectService(BaseService):

    def __init__(self, project_repository: IProjectRepository):
        self._repository = project_repository

    def get_project_by_slug(self, slug: str) -> ProjectDTO:
        """Получение проекта по его slug."""
        return self._repository.get_project_by_slug(slug)

    def create(self, dto: ProjectDTO, user_id: int):
        """Создание нового проекта."""
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

    def update(self, pk, dto, user_id):
        """Обновление существующего проекта."""
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

    def get_project_status_choices(self):
        """Возвращает доступные статусы проекта."""
        return StatusObject.choices()

    def search_projects(self, query: str):
        return self._repository.search_projects(query)
    
    def get_list_participants(self, user_id: id):
        return self._repository.get_list_participants(user_id)


class FeatureService(BaseService):
    def __init__(self, features_repository: IFeaturesRepository):
        self._repository = features_repository

    def get_features_tags_list(self) -> list:
        return self._repository.get_features_tags_list()

    def get_features_status_list(self) -> list:
        return self._repository.get_features_status_list()

    def get_feature_project_list(self) -> list:
        return self._repository.get_feature_project_list()

    def create(self, dto: CreateFeaturesDTO, user_id: int):
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

    def update(self, pk: int, dto, user_id):
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

    def get_search_features(self, query: str):
        return self._repository.get_search_features(query)


class TaskService(BaseService):
    def __init__(self, task_repository: ITaskRepository):
        self._repository = task_repository

    def create(self, dto: CreateTaskDTO, user_id: int):
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

    def update(self, pk: int, dto: TaskDTO, user_id: int):
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

    def get_task_status_choices(self):
        return self._repository.get_task_status_choices()

    def get_tags_list(self, task_id: int):
        return self._repository.get_tags_list(task_id)

    def get_tags_id_list(self, tags_id: int):
        return self._repository.get_tags_id_list(tags_id)

    def get_task_id_list(self, feature: int):
        return self._repository.get_task_id_list(feature)

    def create_comment(self, dto: CommentDTO):
        return self._repository.create_comment(dto)

    def get_comments_list(self, task_id: int):
        return self._repository.get_comments_list(task_id)

    def get_feature_id(self, feature_id: int):
        return self._repository.get_feature_id(feature_id)
    
    def get_list_responsible(self, user_id: int):
        return self._repository.get_list_responsible(user_id)
    
    def get_list_contributor(self, user_id: int):
        return self._repository.get_list_contributor(user_id)
