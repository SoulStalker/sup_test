from .repository import ProjectRepository, TaskRepository
from .dtos import ProjectDTO, TaskDTO

class ProjectService:

    def __init__(self, project_repository: ProjectRepository, task_repository: TaskRepository):
        self.__project_repository = project_repository
        self.__task_repository = task_repository

    def get_project_by_slug(self, slug: str) -> ProjectDTO:
        """Получение проекта по его slug."""
        return self.__project_repository.get_project_by_slug(slug)

    def get_projects_list(self) -> list[ProjectDTO]:
        """Получение списка всех проектов."""
        return self.__project_repository.get_projects_list()

    def get_tasks_by_project(self, project_id: int) -> list[TaskDTO]:
        """Получение задач по идентификатору проекта."""
        return self.__task_repository.get_tasks_by_project(project_id)

    def create_project(self, name: str, slug: str, description: str, status: str) -> ProjectDTO:
        """Создание нового проекта."""
        # Логика для создания проекта, например:
        project = self.__project_repository.create_project(name, slug, description, status)
        return ProjectDTO(
            id=project.id,
            name=project.name,
            slug=project.slug,
            description=project.description,
            status=project.status
        )

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
