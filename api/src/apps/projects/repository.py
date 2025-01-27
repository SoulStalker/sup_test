from abc import ABC

from django.contrib.auth import get_user_model
from django.db.models import Q
from src.apps.base import PermissionMixin
from src.domain.project import (
    CommentDTO,
    CreateFeaturesDTO,
    CreateTaskDTO,
    FeaturesChoicesObject,
    IFeaturesRepository,
    IProjectRepository,
    ITaskRepository,
    ProjectDTO,
    StatusObject,
    TagDTO,
    TaskChoicesObject,
    TaskDTO,
)
from src.domain.project.dtos import FeaturesDTO
from src.models.models import CustomUser
from src.models.projects import Comment, Features, Project, Tags, Task

user = get_user_model()


class ProjectRepository(PermissionMixin, IProjectRepository, ABC):

    model = Project

    @classmethod
    def exists(cls, pk: int) -> bool:
        return cls.model.objects.filter(id=pk).exists()

    def get_list(self) -> list[ProjectDTO]:
        return list(Project.objects.all().order_by("id"))

    def get_project_by_slug(self, slug: str) -> ProjectDTO:
        return Project.objects.get(slug=slug)

    def get_by_id(self, project_id: int) -> ProjectDTO:
        return Project.objects.get(id=project_id)

    def update(self, project_id: int, dto: ProjectDTO) -> ProjectDTO:
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

    def create(self, dto: ProjectDTO) -> ProjectDTO:
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

    def delete(self, pk: int):
        project = Project.objects.get(id=pk)
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


class FeaturesRepository(PermissionMixin, IFeaturesRepository, ABC):

    model = Features

    @classmethod
    def exists(cls, pk: int) -> bool:
        return cls.model.objects.filter(id=pk).exists()

    def get_list(self) -> CreateFeaturesDTO:
        return Features.objects.all().order_by("id")

    def get_features_tags_list(self) -> list:
        return Tags.objects.all().order_by("id")

    def get_features_status_list(self):
        return FeaturesChoicesObject.get_valid_statuses()

    def get_feature_project_list(self) -> list:
        return Project.objects.all().order_by("id")

    def create(self, dto: CreateFeaturesDTO) -> CreateFeaturesDTO:
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
        return CreateFeaturesDTO(
            name=feature.name,
            importance=feature.importance,
            description=feature.description,
            tags=dto.tags,
            participants=dto.participants,
            responsible_id=feature.responsible_id,
            project_id=feature.project_id,
            status=feature.status,
        )

    def get_by_id(self, feature_id: int) -> CreateFeaturesDTO:
        feature = Features.objects.get(id=feature_id)  # может быть исключение
        return FeaturesDTO(
            id=feature.id,
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

    def update(
        self, feature_id: int, dto: CreateFeaturesDTO
    ) -> CreateFeaturesDTO:
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
            feature.participants.set(
                dto.participants
            )  # Передаем список ID участников

        return CreateFeaturesDTO(
            name=feature.name,
            importance=feature.importance,
            description=feature.description,
            tags=dto.tags,
            participants=dto.participants,
            responsible_id=feature.responsible_id,
            project_id=feature.project_id,
            status=feature.status,
        )

    def delete(self, feature_id: int):
        feature = Features.objects.get(id=feature_id)
        feature.delete()

    def get_search_features(self, query: str) -> list[CreateFeaturesDTO]:
        if not query:
            return []
        # Поиск фичей по имени или описанию
        features = Features.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        ).order_by("id")

        return [
            CreateFeaturesDTO(
                name=feature.name,
                importance=feature.importance,
                description=feature.description,
                tags=[
                    tag.id for tag in feature.tags.all()
                ],  # Преобразуем теги в список ID
                participants=[
                    participant.id
                    for participant in feature.participants.all()
                ],
                responsible_id=feature.responsible_id,
                project_id=feature.project_id,
                status=feature.status,
            )
            for feature in features
        ]


class TaskRepository(PermissionMixin, ITaskRepository, ABC):

    model = Task

    @classmethod
    def exists(cls, pk: int) -> bool:
        return cls.model.objects.filter(id=pk).exists()

    @classmethod
    def _task_orm_to_dto(cls, task: Task) -> TaskDTO:
        return TaskDTO(
            id=task.id,
            name=task.name,
            priority=task.priority,
            tags=[
                tag.id for tag in task.tags.all()
            ],  # Преобразуем теги в список ID
            contributor_id=task.contributor_id,
            responsible_id=task.responsible_id,
            status=task.status,
            created_at=task.created_at,
            closed_at=task.closed_at,
            description=task.description,
            feature_id=task.feature_id,
        )

    def get_list(self) -> TaskDTO:
        return Task.objects.all().order_by("id")

    def get_by_id(self, task_id: int) -> TaskDTO:
        return self._task_orm_to_dto(Task.objects.get(id=task_id))

    def create(self, dto: CreateTaskDTO):
        task = self.model(
            name=dto.name,
            priority=dto.priority,
            contributor_id=dto.contributor_id,
            responsible_id=dto.responsible_id,
            status=dto.status,
            feature_id=dto.feature_id,
            description=dto.description,
        )

        task.save()
        task.tags.set(dto.tags)

    def update(self, dto: TaskDTO) -> TaskDTO:
        task = Task.objects.get(id=dto.id)

        task.name = dto.name
        task.priority = dto.priority
        task.contributor_id = dto.contributor_id
        task.responsible_id = dto.responsible_id
        task.status = dto.status
        task.feature_id = dto.feature_id
        task.description = dto.description
        task.save()
        task.tags.set(dto.tags)

    def delete(self, task_id: int):
        task = Task.objects.get(id=task_id)
        task.delete()

    def get_task_status_choices(self):
        return TaskChoicesObject.choices()

    def get_tags_list(self, task_id: int) -> list[TagDTO]:
        task = Task.objects.get(id=task_id)
        tags = task.tags.all()
        return [
            TagDTO(id=tag.id, name=tag.name, color=tag.color) for tag in tags
        ]

    def get_tags_id_list(self, tags_id: int):
        tags = Tags.objects.filter(id__in=tags_id)
        return tags

    def get_task_id_list(self, feature: int):
        feature_instance = Features.objects.get(name=feature.name)
        task = feature_instance.tasks_features.all()
        return task

    def create_comment(self, dto: CommentDTO):
        comment = Comment(
            user=CustomUser.objects.get(id=dto.user_id),
            comment=dto.comment,
            task=Task.objects.get(id=dto.task_id),
        )
        comment.save()

    def get_comments_list(self, task_id):
        task = Task.objects.get(id=task_id)
        comments = Comment.objects.filter(task=task)
        return comments
