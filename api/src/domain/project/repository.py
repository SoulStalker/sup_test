from .dtos import ProjectDTO
import abc

class IProjectRepository(abc.ABC):
    @abc.abstractmethod
    def create_project(self, dto: ProjectDTO) -> ProjectDTO:
        pass

    @abc.abstractmethod
    def update_project(self, project_id: int, name: str, slug: str, description: str, status: str) -> ProjectDTO:
        pass

    @abc.abstractmethod
    def delete_project(self, project_id: int):
        pass

    @abc.abstractmethod
    def get_project_list(self) -> list[ProjectDTO]:
        pass

    @abc.abstractmethod
    def get_project_by_slug(self, slug: str) -> ProjectDTO:
        pass

    @abc.abstractmethod
    def get_project_by_id(self, project_id: int) -> ProjectDTO:
        pass