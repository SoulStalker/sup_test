from abc import ABC
from src.domain.project.dtos import ProjectDTO, StatusObject, FeaturesDTO, FeaturesChoicesObject
from src.domain.project.repository import IProjectRepository, IFeaturesRepository
from src.models.projects import Project, Features
from django.db.models import Q

class ProjectRepository(IProjectRepository, ABC):

    model = Project

    def get_project_list(self) -> list[ProjectDTO]:
        return list(Project.objects.all().order_by('id'))

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
            date_created=project.date_created
        )

    def create_project(self, dto: ProjectDTO) -> ProjectDTO:
        project = Project.objects.create(
            name=dto.name,
            logo=dto.logo,
            description=dto.description,
            status=dto.status,
            responsible_id=dto.responsible_id,
            date_created=dto.date_created
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
            date_created=project.date_created
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
        ).order_by('id')

        return [ProjectDTO(
            name=project.name,
            slug=project.slug,
            description=project.description,
            status=project.status,
            responsible_id=project.responsible_id,
            participants=project.participants.all(),
            date_created=project.date_created
        ) for project in projects]


class FeaturesRepository(IFeaturesRepository, ABC):

    model = Features

    def get_Featuress_list(self) -> FeaturesDTO:
        return Features.objects.all().order_by('id')