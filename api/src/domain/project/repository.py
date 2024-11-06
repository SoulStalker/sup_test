import abc

from .dtos import ProjectDTO


class IProjectRepository(abc.ABC):
    @abc.abstractmethod
    def create_project(self, dto: ProjectDTO) -> ProjectDTO:
        pass

    @abc.abstractmethod
    def update_project(
        self,
        project_id: int,
        name: str,
        slug: str,
        description: str,
        status: str,
    ) -> ProjectDTO:
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

    @abc.abstractmethod
    def get_valid_statuses(self) -> list:
        """Возвращает все допустимые статусы."""
        pass

    @abc.abstractmethod
    def status_orm_to_dto(self, status: str) -> str:
        """Преобразует статус в DTO."""
        pass
