from abc import abstractmethod

from src.domain.base import BaseRepository
from src.domain.user.dtos import CreateRoleDTO, PermissionDTO, RoleDTO, UserDTO
from src.domain.user.entity import CreatePermissionEntity, CreateUserEntity


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
    def create(self, dto: CreatePermissionEntity):
        raise NotImplementedError

    @abstractmethod
    def update(self, permission_id: int, dto: PermissionDTO):
        raise NotImplementedError

    @abstractmethod
    def get_permission_by_code(self, code):
        raise NotImplementedError

    def get_content_types(self):
        raise NotImplementedError

    def get_content_object(self, permission_id):
        raise NotImplementedError

    def get_content_objects(self):
        raise NotImplementedError

    def get_codes(self):
        raise NotImplementedError

    def get_objects_data(self, content_type_id):
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
