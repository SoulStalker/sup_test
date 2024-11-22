import abc

from src.domain.user.dtos import (
    CreatePermissionDTO,
    CreateRoleDTO,
    CreateUserDTO,
    PermissionDTO,
    RoleDTO,
    UserDTO,
)


class IRoleRepository(abc.ABC):
    @abc.abstractmethod
    def get_role_by_id(self, role_id: int) -> RoleDTO:
        raise NotImplementedError

    @abc.abstractmethod
    def get_role_list(self) -> list[RoleDTO]:
        raise NotImplementedError

    @abc.abstractmethod
    def create(self, dto: CreateRoleDTO):
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, role_id: int, dto: RoleDTO):
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, role_id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def get_roles_participants_count(self, role_id: int) -> int:
        raise NotImplementedError


class IPermissionRepository(abc.ABC):
    @abc.abstractmethod
    def get_permission_by_id(self, permission_id: int) -> PermissionDTO:
        raise NotImplementedError

    @abc.abstractmethod
    def get_permission_list(self) -> list[PermissionDTO]:
        raise NotImplementedError

    @abc.abstractmethod
    def create(self, dto: CreatePermissionDTO):
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, permission_id: int, dto: PermissionDTO):
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, permission_id: int):
        raise NotImplementedError


class IUserRepository(abc.ABC):
    @abc.abstractmethod
    def get_user_by_id(self, user_id: int) -> UserDTO:
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_list(self) -> list[UserDTO]:
        raise NotImplementedError

    @abc.abstractmethod
    def create(self, dto: CreateUserDTO):
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, user_id: int, dto: UserDTO):
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, user_id: int):
        raise NotImplementedError
