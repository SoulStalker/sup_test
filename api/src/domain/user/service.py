from src.domain.base import BaseService
from src.domain.user.dtos import CreatePermissionDTO, UserDTO
from src.domain.user.entity import CreatePermissionEntity, CreateUserEntity
from src.domain.user.repository import (
    IPermissionRepository,
    IRoleRepository,
    IUserRepository,
)


class RoleService(BaseService):
    def __init__(self, repository: IRoleRepository):
        self._repository = repository

    def create(self, dto, user_id):
        entity = dto
        return self.validate_and_save(entity, self._repository, dto, user_id)

    def update(self, pk, dto, user_id):
        entity = dto
        return self.validate_and_update(
            entity, self._repository, dto, pk, user_id
        )

    def get_roles_participants_count(self, role_id: int):
        return self._repository.get_roles_participants_count(role_id)


class PermissionService(BaseService):
    def __init__(self, repository: IPermissionRepository):
        self._repository = repository

    def create(self, dto: CreatePermissionDTO, user_id: int):
        entity = CreatePermissionEntity(
            name=dto.name,
            code=dto.code,
            description=dto.description,
            content_type=dto.content_type,
            object_id=dto.object_id,
        )
        return self.validate_and_save(entity, self._repository, dto, user_id)

    def update(self, pk, dto, user_id):
        entity = dto
        return self.validate_and_update(
            entity, self._repository, dto, pk, user_id
        )

    def get_content_types(self):
        return self._repository.get_content_types()

    def get_content_object(self, permission_id: int):
        return self._repository.get_content_object(permission_id)

    def get_content_objects(self):
        return self._repository.get_content_objects()

    def get_codes(self):
        return self._repository.get_codes()

    def get_objects_data(self, content_type_id: int):
        return self._repository.get_objects_data(content_type_id)


class UserService(BaseService):
    def __init__(self, repository: IUserRepository):
        self._repository = repository

    def create(self, dto: CreateUserEntity, user_id: int):
        entity = dto
        # dto.password = dto.generate_password()
        return self.validate_and_save(entity, self._repository, dto, user_id)

    def update(self, pk, dto, user_id):
        entity = dto
        return self.validate_and_update(
            entity, self._repository, dto, pk, user_id
        )

    def create_user_with_generated_password(self, dto: UserDTO):
        password = self.generate_password()
        user = self._repository.create(dto)
        user.set_password(password)
        user.save()
        return user

    def send_welcome_email(self, user_dto):
        self._repository.send_welcome_email(user_dto)

    def get_user_id_list(self, user_list_id: list):
        self._repository.get_user_id_list(user_list_id)
