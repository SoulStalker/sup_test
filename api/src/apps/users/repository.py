from abc import ABC

from django.shortcuts import get_list_or_404, get_object_or_404
from src.domain.user.dtos import PermissionDTO, RoleDTO, UserDTO
from src.domain.user.repository import (
    IPermissionRepository,
    IRoleRepository,
    IUserRepository,
)

from api.src.models.models import CustomUser, Permission, Role


class RoleRepository(IRoleRepository, ABC):
    model = Role

    def _role_orm_to_dto(self, role: Role) -> RoleDTO:
        return RoleDTO(
            id=role.id,
            name=role.name,
            color=role.color,
        )

    def _get_role_by_id(self, role_id: int) -> Role:
        return get_object_or_404(self.model, id=role_id)

    def create(self, dto: RoleDTO) -> RoleDTO:
        model = self.model(
            name=dto.name,
            color=dto.color,
        )

        model.save()
        return self._role_orm_to_dto(model)

    def update(self, role_id: int, dto: RoleDTO) -> RoleDTO:
        model = self._get_role_by_id(role_id)
        model.name = dto.name
        model.color = dto.color

        model.save()
        return self._role_orm_to_dto(model)

    def delete(self, role_id: int):
        model = self._get_role_by_id(role_id)
        model.delete()

    def get_role_by_id(self, role_id: int) -> RoleDTO:
        model = self._get_role_by_id(role_id)
        return self._role_orm_to_dto(model)

    def get_role_list(self) -> list[RoleDTO]:
        models = get_list_or_404(self.model)
        return [self._role_orm_to_dto(model) for model in models]


class PermissionRepository(IPermissionRepository, ABC):
    model = Permission

    def _permission_orm_to_dto(self, permission: Permission) -> PermissionDTO:
        return PermissionDTO(
            id=permission.id,
            name=permission.name,
            description=permission.description,
        )

    def _get_permission_by_id(self, permission_id: int) -> Permission:
        return get_object_or_404(self.model, id=permission_id)

    def create(self, dto: PermissionDTO) -> PermissionDTO:
        model = self.model(
            name=dto.name,
            description=dto.description,
        )
        model.save()
        return self._permission_orm_to_dto(model)

    def update(self, permission_id: int, dto: PermissionDTO) -> PermissionDTO:
        model = self._get_permission_by_id(permission_id)
        model.name = dto.name
        model.description = dto.description

        model.save()
        return self._permission_orm_to_dto(model)

    def delete(self, permission_id: int):
        model = self._get_permission_by_id(permission_id)
        model.delete()

    def get_permission_by_id(self, permission_id: int) -> PermissionDTO:
        model = self._get_permission_by_id(permission_id)
        return self._permission_orm_to_dto(model)

    def get_permission_list(self) -> list[PermissionDTO]:
        models = get_list_or_404(self.model)
        return [self._permission_orm_to_dto(model) for model in models]


class UserRepository(IUserRepository, ABC):
    model = CustomUser

    def _user_orm_to_dto(self, user: CustomUser) -> UserDTO:
        return UserDTO(
            id=user.id,
            name=user.name,
            surname=user.surname,
            email=user.email,
            tg_name=user.tg_name,
            tg_nickname=user.tg_nickname,
            google_meet_nickname=user.google_meet_nickname,
            gitlab_nickname=user.gitlab_nickname,
            github_nickname=user.github_nickname,
            avatar=user.avatar,
            role_id=user.role,
            permission_id=user.permissions,
            is_active=user.is_active,
            is_admin=user.is_admin,
            is_superuser=user.is_superuser,
            is_staff=user.is_staff,
        )

    def _get_user_by_id(self, user_id: int) -> CustomUser:
        return get_object_or_404(self.model, id=user_id)

    def create(self, dto: UserDTO) -> UserDTO:
        model = self.model(
            id=dto.id,
            name=dto.name,
            surname=dto.surname,
            email=dto.email,
            tg_name=dto.tg_name,
            tg_nickname=dto.tg_nickname,
            google_meet_nickname=dto.google_meet_nickname,
            gitlab_nickname=dto.gitlab_nickname,
            github_nickname=dto.github_nickname,
            avatar=dto.avatar,
            role_id=dto.role,
            permission_id=dto.permissions,
            is_active=dto.is_active,
            is_admin=dto.is_admin,
            is_superuser=dto.is_superuser,
            is_staff=dto.is_staff,
        )
        model.save()
        return self._user_orm_to_dto(model)

    def update(self, user_id: int, dto: UserDTO) -> UserDTO:
        model = self._get_user_by_id(user_id)
        model.name = dto.name
        model.surname = dto.surname
        model.email = dto.email
        model.tg_name = dto.tg_name
        model.tg_nickname = dto.tg_nickname
        model.google_meet_nickname = dto.google_meet_nickname
        model.gitlab_nickname = dto.gitlab_nickname
        model.github_nickname = dto.github_nickname
        model.avatar = dto.avatar
        model.role = dto.role_id
        model.permissions = dto.permission_id
        model.is_active = dto.is_active
        model.is_admin = dto.is_admin
        model.is_superuser = dto.is_superuser
        model.is_staff = dto.is_staff

        model.save()
        return self._user_orm_to_dto(model)

    def delete(self, user_id: int):
        model = self._get_user_by_id(user_id)
        model.delete()

    def get_user_by_id(self, user_id: int) -> UserDTO:
        model = self._get_user_by_id(user_id)
        return self._user_orm_to_dto(model)

    def get_user_list(self) -> list[UserDTO]:
        models = get_list_or_404(self.model)
        return [self._user_orm_to_dto(model) for model in models]
