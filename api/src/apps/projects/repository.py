from abc import ABC
from src.domain.project.dtos import ProjectDTO
from src.domain.project.repository import IProjectRepository
from src.models.projects import Project

class ProjectRepository(IProjectRepository, ABC):

    model = Project

    def get_project_list(self) -> list[ProjectDTO]:
        return list(Project.objects.all())

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
            slug=dto.slug,
            description=dto.description,
            status=dto.status
        )
        return ProjectDTO(
            id=project.id,
            name=project.name,
            slug=project.slug,
            description=project.description,
            status=project.status
        )

    def delete_project(self, project_id: int):
        project = Project.objects.get(id=project_id)
        project.delete()


