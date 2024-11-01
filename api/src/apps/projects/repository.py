from abc import ABC
from src.domain.project.dtos import ProjectDTO, StatusObject
from src.domain.project.repository import IProjectRepository
from src.models.projects import Project

class ProjectRepository(IProjectRepository, ABC):

    model = Project

    def get_project_list(self) -> list[ProjectDTO]:
        return list(Project.objects.all().order_by('id'))

    def get_project_by_slug(self, slug: str) -> ProjectDTO:
        return Project.objects.get(slug=slug)

    def get_project_by_id(self, project_id: int) -> ProjectDTO:
        return Project.objects.get(id=project_id)

    def update_project(self, project_id: int, name: str, slug: str, description: str, status: str) -> ProjectDTO:
        project = Project.objects.get(id=project_id)
        project.name = name
        project.slug = slug
        project.description = description
        project.status = status
        project.save()
        return ProjectDTO(
            id=project.id,
            name=project.name,
            slug=project.slug,
            description=project.description,
            status=project.status
        )

    def create_project(self, dto: ProjectDTO) -> ProjectDTO:
        project = Project.objects.create(
            name=dto.name,
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

