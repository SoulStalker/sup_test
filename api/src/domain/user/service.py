from src.domain.user.dtos import (
    CreatePermissionDTO,
    CreateRoleDTO,
    PermissionDTO,
    RoleDTO,
    TeamDTO,
    UserDTO,
)
from src.domain.user.entity import CreateUserEntity
from src.domain.user.repository import (
    IPermissionRepository,
    IRoleRepository,
    ITeamRepository,
    IUserRepository,
)


class RoleService:
    def __init__(self, repository: IRoleRepository):
        self.__repository = repository

    def get_role(self, role_id: int) -> RoleDTO:
        return self.__repository.get_role_by_id(role_id)

    def get_role_list(self) -> list[RoleDTO]:
        return self.__repository.get_role_list()

    def create(self, dto: CreateRoleDTO):
        self.__repository.create(dto)

    def update(self, role_id: int, dto: RoleDTO):
        self.__repository.update(role_id, dto)

    def delete(self, role_id: int):
        self.__repository.delete(role_id)

    def get_roles_participants_count(self, role_id: int):
        return self.__repository.get_roles_participants_count(role_id)


class PermissionService:
    def __init__(self, repository: IPermissionRepository):
        self.__repository = repository

    def get_permission(self, permission_id: int) -> PermissionDTO:
        return self.__repository.get_permission_by_id(permission_id)

    def get_permission_list(self) -> list[PermissionDTO]:
        return self.__repository.get_permission_list()

    def create(self, dto: CreatePermissionDTO):
        self.__repository.create(dto)

    def update(self, permission_id: int, dto: PermissionDTO):
        self.__repository.update(permission_id, dto)

    def delete(self, permission_id: int):
        self.__repository.delete(permission_id)


class UserService:
    def __init__(self, repository: IUserRepository):
        self.__repository = repository

    def get_user(self, user_id: int) -> UserDTO:
        return self.__repository.get_user_by_id(user_id)

    def get_user_list(self) -> list[UserDTO]:
        return self.__repository.get_user_list()

    def create(self, dto: CreateUserEntity):
        dto.password = dto.generate_password()
        self.__repository.create(dto)

    def update(self, user_id: int, dto: UserDTO):
        self.__repository.update(user_id, dto)

    def delete(self, user_id: int):
        self.__repository.delete(user_id)

    def change_password(self, user_id: int, new_password: str):
        user = self.__repository.get_user_by_id(user_id)
        user.set_password(new_password)
        user.save()

    # def generate_password(self) -> str:
    #     return secrets.choice(string.ascii_letters + string.digits)

    def create_user_with_generated_password(self, dto: UserDTO):
        password = self.generate_password()
        user = self.__repository.create(dto)
        user.set_password(password)
        user.save()
        return user

    def set_password_registration(self, user_email, password1, password2):
        self.__repository.set_password_registration(user_email, password1, password2)

        
class TeamService:
    def __init__(self, repository: ITeamRepository):
        self.__repository = repository

    def get_team_list(self) -> list[TeamDTO]:
        return self.__repository.get_team_list()
