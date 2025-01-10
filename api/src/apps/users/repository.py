import os
from abc import ABC

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_list_or_404, get_object_or_404
from src.domain.user import (
    CreatePermissionDTO,
    CreateRoleDTO,
    CreateUserEntity,
    IPermissionRepository,
    IRoleRepository,
    IUserRepository,
    PermissionDTO,
    RoleDTO,
    UserDTO,
)
from src.models.models import CustomUser, Permission, Role


class RoleRepository(IRoleRepository, ABC):
    model = Role

    def _role_orm_to_dto(self, role: Role) -> RoleDTO:
        return RoleDTO(
            id=role.id,
            name=role.name,
            color=role.color,
        )

    def exists(self, pk: int) -> bool:
        return self.model.objects.filter(id=pk).exists()

    def get_by_id(self, role_id: int) -> Role:
        role = get_object_or_404(self.model, id=role_id)
        return role

    def create(self, dto: CreateRoleDTO) -> RoleDTO:
        role = self.model(
            name=dto.name,
            color=dto.color,
        )

        role.save()
        return self._role_orm_to_dto(role)

    def update(self, role_id: int, dto: RoleDTO) -> RoleDTO:
        role = get_object_or_404(self.model, id=role_id)
        role.name = dto.name
        role.color = dto.color

        role.save()
        return self._role_orm_to_dto(role)

    def delete(self, role_id: int):
        role = get_object_or_404(self.model, id=role_id)
        role.delete()

    def get_list(self) -> list[RoleDTO]:
        roles = get_list_or_404(self.model)
        return [self._role_orm_to_dto(role) for role in roles]

    def get_roles_participants_count(self, role_id: int) -> int:
        participants = CustomUser.objects.filter(role_id=role_id).count()
        return participants


class PermissionRepository(IPermissionRepository, ABC):
    model = Permission

    def _permission_orm_to_dto(self, permission: Permission) -> PermissionDTO:
        return PermissionDTO(
            id=permission.id,
            code=permission.code,
            name=permission.name,
            description=permission.description,
        )

    def exists(self, pk: int) -> bool:
        return self.model.objects.filter(id=pk).exists()

    def get_by_id(self, permission_id: int) -> PermissionDTO:
        model = get_object_or_404(self.model, id=permission_id)
        return self._permission_orm_to_dto(model)

    def create(self, dto: CreatePermissionDTO) -> PermissionDTO:
        model = self.model(
            name=dto.name,
            code=dto.code,
            description=dto.description,
        )
        model.save()
        return self._permission_orm_to_dto(model)

    def update(self, permission_id: int, dto: PermissionDTO) -> PermissionDTO:
        model = get_object_or_404(self.model, id=permission_id)
        model.name = dto.name
        model.code = dto.code
        model.description = dto.description

        model.save()
        return self._permission_orm_to_dto(model)

    def delete(self, permission_id: int):
        model = get_object_or_404(self.model, id=permission_id)
        model.delete()

    def get_list(self) -> list[PermissionDTO]:
        models = get_list_or_404(self.model)
        return [self._permission_orm_to_dto(model) for model in models]


class UserRepository(IUserRepository, ABC):
    model = CustomUser
    avatar_path = os.path.join(settings.MEDIA_ROOT, "images", "avatars")

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
            team_id=user.team,
            permissions_ids=list(
                user.permissions.values_list("id", flat=True)
            ),
            is_active=user.is_active,
            is_admin=user.is_admin,
            is_superuser=user.is_superuser,
            date_joined=user.date_joined,
            # meets_ids=list(user.meets.values_list("id", flat=True)),
            meet_statuses={
                meet.id: meet_participant.status_color
                for meet in user.meets.all()
                for meet_participant in meet.meetparticipant_set.all()
                if meet_participant.custom_user == user
            },
        )

    def exists(self, pk: int) -> bool:
        return self.model.objects.filter(id=pk).exists()

    def create(self, dto: CreateUserEntity) -> UserDTO:
        model = CustomUser.objects.create(
            name=dto.name,
            surname=dto.surname,
            email=dto.email,
            tg_name=dto.tg_name,
            tg_nickname=dto.tg_nickname,
            google_meet_nickname=dto.google_meet_nickname,
            gitlab_nickname=dto.gitlab_nickname,
            github_nickname=dto.github_nickname,
            avatar=dto.avatar,
            role_id=dto.role_id,
            team_id=dto.team_id,
            is_active=dto.is_active,
            is_admin=dto.is_admin,
            is_superuser=dto.is_superuser,
        )

        # установка прав пользователю
        model.permissions.set(dto.permissions_ids)
        # шифрование пароля
        model.set_password(dto.password)
        model.save()
        return self._user_orm_to_dto(model)

    def update(self, user_id: int, dto: UserDTO) -> UserDTO:
        model = get_object_or_404(self.model, id=user_id)
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
        model.team = dto.team_id
        model.permissions.set(dto.permissions_ids)
        model.is_active = dto.is_active
        model.is_admin = dto.is_admin
        model.is_superuser = dto.is_superuser

        model.save()

        return self._user_orm_to_dto(model)

    def delete(self, user_id: int):
        model = get_object_or_404(self.model, id=user_id)
        model.delete()

    def get_by_id(self, user_id: int) -> UserDTO:
        model = get_object_or_404(self.model, id=user_id)
        return self._user_orm_to_dto(model)

    def get_list(self) -> list[UserDTO]:
        models = get_list_or_404(self.model)
        return [self._user_orm_to_dto(model) for model in models]
    
    def get_user_id_list(self, user_id: int) -> list[UserDTO]:
        user = self.model.objects.filter(id__in=user_id)
        return user

    def send_welcome_email(self, user_dto):
        subject = "Добро пожаловать!"
        message = (
            f"Здравствуйте, {user_dto.name}!\n\nВаш аккаунт успешно создан."
        )
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user_dto.email]
        send_mail(
            subject, message, from_email, recipient_list, fail_silently=False
        )
