from .repository import IProjectRepository
from src.domain.project.entity import ProjectEntity
from .dtos import ProjectDTO, StatusObject

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

    def update_project(self, project_id: int, name: str, slug: str, description: str, status: str) -> ProjectDTO:
        """Обновление существующего проекта."""
        project = self.__project_repository.update_project(project_id, name, slug, description, status)
        return ProjectDTO(
            id=project.id,
            name=project.name,
            slug=project.slug,
            description=project.description,
            status=project.status
        )

    def delete_project(self, project_id: int):
        """Удаление существующего проекта."""
        return self.__project_repository.delete_project(project_id)

    def get_project_status_choices(self):
        """Возвращает доступные статусы проекта."""
        return StatusObject.choices()

