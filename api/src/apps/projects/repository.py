from abc import ABC

from django.db.models import Q

from src.domain.project.dtos import (
    ProjectDTO,
    StatusObject,
    FeaturesDTO,
    FeaturesChoicesObject,
)
from src.domain.project.repository import (
    IProjectRepository,
    IFeaturesRepository,
    ITaskRepository,
)
from src.models.projects import Project, Features, Tags, Task
from src.domain.project.dtos import TaskDTO


class ProjectRepository(IProjectRepository, ABC):

    model = Project

    def get_project_list(self) -> list[ProjectDTO]:
        return list(Project.objects.all().order_by("id"))

    def get_project_by_slug(self, slug: str) -> ProjectDTO:
        return Project.objects.get(slug=slug)

    def get_project_by_id(self, project_id: int) -> ProjectDTO:
        return Project.objects.get(id=project_id)

    def update_project(self, project_id: int, dto: ProjectDTO) -> ProjectDTO:
        project = Project.objects.get(id=project_id)
        project.name = dto.name
        project.logo = dto.logo
        project.slug = dto.slug
        project.description = dto.description
        project.status = dto.status
        project.responsible_id = dto.responsible_id
        project.date_created = dto.date_created
        project.participants.set(dto.participants)
        project.save()

        return ProjectDTO(
            name=project.name,
            logo=project.logo.url if project.logo else None,
            slug=project.slug,
            description=project.description,
            status=project.status,
            responsible_id=project.responsible_id,
            participants=dto.participants,
            date_created=project.date_created,
        )

    def create_project(self, dto: ProjectDTO) -> ProjectDTO:
        project = Project.objects.create(
            name=dto.name,
            logo=dto.logo,
            description=dto.description,
            status=dto.status,
            responsible_id=dto.responsible_id,
            date_created=dto.date_created,
        )

        # Устанавливаем участников сразу при создании проекта
        if dto.participants:
            project.participants.set(dto.participants)

        # Возвращаем созданный объект в виде ProjectDTO
        return ProjectDTO(
            name=project.name,
            logo=project.logo.url if project.logo else None,
            slug=project.slug,
            description=project.description,
            status=project.status,
            responsible_id=project.responsible_id,
            participants=dto.participants,
            date_created=project.date_created,
        )

    def delete_project(self, project_id: int):
        project = Project.objects.get(id=project_id)
        project.delete()

    def get_valid_statuses(self):
        """Возвращает все допустимые статусы."""
        return StatusObject.get_valid_statuses()

    def status_orm_to_dto(self, status: str) -> str:
        """Возвращает статус как строку (в данном случае он уже строка)."""
        return status

    def search_projects(self, query: str) -> list[ProjectDTO]:
        if not query:
            return []
        # Поиск проектов по имени или описанию
        projects = Project.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        ).order_by("id")

        return [
            ProjectDTO(
                name=project.name,
                slug=project.slug,
                description=project.description,
                status=project.status,
                responsible_id=project.responsible_id,
                participants=project.participants.all(),
                date_created=project.date_created,
            )
            for project in projects
        ]


class FeaturesRepository(IFeaturesRepository, ABC):

    model = Features

    def get_features_list(self) -> FeaturesDTO:
        return Features.objects.all().order_by("id")

    def get_features_tags_list(self) -> list:
        return Tags.objects.all().order_by("id")

    def get_features_status_list(self):
        return FeaturesChoicesObject.get_valid_statuses()

    def get_feature_project_list(self) -> list:
        return Project.objects.all().order_by("id")

    def create_feature(self, dto: FeaturesDTO) -> FeaturesDTO:
        # Создаем объект Features без тегов
        feature = Features.objects.create(
            name=dto.name,
            importance=dto.importance,
            description=dto.description,
            responsible_id=dto.responsible_id,
            project_id=dto.project_id,
            status=dto.status,
        )

        if dto.tags:
            feature.tags.set(dto.tags)

        if dto.participants:
            feature.participants.set(dto.participants)

        # Возвращаем созданный объект в виде FeaturesDTO без тегов
        return FeaturesDTO(
            name=feature.name,
            importance=feature.importance,
            description=feature.description,
            tags=dto.tags,
            participants=dto.participants,
            responsible_id=feature.responsible_id,
            project_id=feature.project_id,
            status=feature.status,
        )

    def get_feature_by_id(self, feature_id: int) -> FeaturesDTO:
        feature = Features.objects.get(id=feature_id)  # может быть исключение
        return FeaturesDTO(
            name=feature.name,
            importance=feature.importance,
            description=feature.description,
            tags=[tag.id for tag in feature.tags.all()],  # Преобразуем теги в список ID
            participants=[participant.id for participant in feature.participants.all()],
            responsible_id=feature.responsible_id,
            project_id=feature.project_id,
            status=feature.status,
        )

    def update_features(self, feature_id: int, dto: FeaturesDTO) -> FeaturesDTO:
        try:
            feature = Features.objects.get(id=feature_id)
        except Features.DoesNotExist:
            raise ValueError(f"Feature with ID {feature_id} not found")

        feature.name = dto.name
        feature.importance = dto.importance
        feature.description = dto.description
        feature.responsible_id = dto.responsible_id
        feature.project_id = dto.project_id
        feature.status = dto.status
        feature.save()

        if dto.tags:
            feature.tags.set(dto.tags)  # Передаем список ID тегов

        if dto.participants:
            feature.participants.set(dto.participants)  # Передаем список ID участников

        return FeaturesDTO(
            name=feature.name,
            importance=feature.importance,
            description=feature.description,
            tags=dto.tags,
            participants=dto.participants,
            responsible_id=feature.responsible_id,
            project_id=feature.project_id,
            status=feature.status,
        )

    def delete_features(self, feature_id: int):
        feature = Features.objects.get(id=feature_id)
        feature.delete()

    def get_search_features(self, query: str) -> list[FeaturesDTO]:
        if not query:
            return []
        # Поиск фичей по имени или описанию
        features = Features.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        ).order_by("id")

        return [
            FeaturesDTO(
                name=feature.name,
                importance=feature.importance,
                description=feature.description,
                tags=[
                    tag.id for tag in feature.tags.all()
                ],  # Преобразуем теги в список ID
                participants=[
                    participant.id for participant in feature.participants.all()
                ],
                responsible_id=feature.responsible_id,
                project_id=feature.project_id,
                status=feature.status,
            )
            for feature in features
        ]


class TaskRepository(ITaskRepository, ABC):

    model = Task

    def get_tasks_list(self) -> TaskDTO:
        return Task.objects.all().order_by("id")

    def get_task_by_id(self, task_id: int) -> TaskDTO:
        return Task.objects.get(id=task_id)

    def create_task(self, dto: TaskDTO) -> TaskDTO:
        task = Task.objects.create(
            name=dto.name,
            logo=dto.logo,
            description=dto.description,
            status=dto.status,
            responsible_id=dto.responsible_id,
            date_created=dto.date_created,
        )

        if dto.participants:
            task.participants.set(dto.participants)

        return TaskDTO(
            name=task.name,
            logo=task.logo,
            description=task.description,
            status=task.status,
            responsible_id=task.responsible_id,
            participants=dto.participants,
            date_created=task.date_created,
        )

    def update_task(self, task_id: int, dto: TaskDTO) -> TaskDTO:
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise ValueError(f"Task with ID {task_id} not found")

        task.name = dto.name
        task.logo = dto.logo
        task.description = dto.description
        task.status = dto.status
        task.responsible_id = dto.responsible_id
        task.date_created = dto.date_created
        task.save()

    def delete_task(self, task_id: int):
        task = Task.objects.get(id=task_id)
        task.delete()
