from dataclasses import dataclass
from datetime import datetime


@dataclass
class CreateRoleDTO:
    name: str
    color: str


@dataclass
class RoleDTO(CreateRoleDTO):
    id: int


@dataclass
class CreatePermissionDTO:
    name: str
    code: str
    description: str
    content_type: str
    object_id: int | None


@dataclass
class PermissionDTO(CreatePermissionDTO):
    id: int


@dataclass
class UserDTO:
    id: int
    name: str
    surname: str
    email: str
    tg_name: str
    tg_nickname: str
    google_meet_nickname: str
    gitlab_nickname: str
    github_nickname: str
    avatar: str | None
    role_id: int
    team_id: int | None
    permissions_ids: list[int]
    is_active: bool | None
    is_admin: bool | None
    is_superuser: bool | None
    date_joined: datetime | None
    meet_statuses: dict[int:str] | None
