from abc import abstractmethod

from src.domain.base import BaseRepository
from src.domain.user.dtos import (
    CreatePermissionDTO,
    CreateRoleDTO,
    PermissionDTO,
    RoleDTO,
    UserDTO,
)
from src.domain.user.entity import CreateUserEntity


class IRoleRepository(BaseRepository):

    @abstractmethod
    def create(self, dto: CreateRoleDTO):
        raise NotImplementedError

    @abstractmethod
    def update(self, role_id: int, dto: RoleDTO):
        raise NotImplementedError

    @abstractmethod
    def get_roles_participants_count(self, role_id: int) -> int:
        raise NotImplementedError


class IPermissionRepository(BaseRepository):

    @abstractmethod
    def create(self, dto: CreatePermissionDTO):
        raise NotImplementedError

    @abstractmethod
    def update(self, permission_id: int, dto: PermissionDTO):
        raise NotImplementedError

    @abstractmethod
    def get_permission_by_code(self, code):
        raise NotImplementedError


class IUserRepository(BaseRepository):
    @abstractmethod
    def create(self, dto: CreateUserEntity):
        raise NotImplementedError

    @abstractmethod
    def update(self, user_id: int, dto: UserDTO):
        raise NotImplementedError

    @abstractmethod
    def delete(self, user_id: int):
        raise NotImplementedError

    @abstractmethod
    def send_welcome_email(self, user_dto):
        raise NotImplementedError
