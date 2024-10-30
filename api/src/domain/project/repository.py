from src.models.projects import Project, Task
from .dtos import ProjectDTO, TaskDTO

class ProjectRepository:
    @staticmethod
    def get_project_by_slug(slug: str) -> ProjectDTO:
        project = Project.objects.get(slug=slug)
        return ProjectDTO(
            id=project.id,
            name=project.name,
            slug=project.slug,
            description=project.description,
            status=project.status
        )

    @staticmethod
    def get_projects_list() -> list[ProjectDTO]:
        projects = Project.objects.all()
        return [
            ProjectDTO(
                id=project.id,
                name=project.name,
                slug=project.slug,
                description=project.description,
                status=project.status,
                date_created=project.date_created,
                participants=project.participants
            ) for project in projects
        ]

class TaskRepository:
    @staticmethod
    def get_tasks_by_project(project_id: int) -> list[TaskDTO]:
        tasks = Task.objects.filter(project_id=project_id)
        return [
            TaskDTO(
                id=task.id,
                name=task.name,
                slug=task.slug,
                description=task.description,
                status=task.status,
                date_execution=task.date_execution
            ) for task in tasks
        ]
