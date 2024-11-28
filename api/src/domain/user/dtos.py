from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class RoleDTO:
    id: int
    name: str
    color: str


@dataclass
class CreateRoleDTO:
    name: str
    color: str


@dataclass
class TeamDTO:
    id: int
    name: str


@dataclass
class PermissionDTO:
    id: int
    name: str
    code: int
    description: str


@dataclass
class CreatePermissionDTO:
    name: str
    code: int
    description: str


@dataclass
class UserDTO:
    # id: int
    name: str
    surname: str
    email: str
    tg_name: str
    tg_nickname: str
    google_meet_nickname: str
    gitlab_nickname: str
    github_nickname: str
    avatar: Optional[str]
    role_id: int
    team_id: Optional[int]
    permissions_ids: list[int]
    is_active: Optional[bool]
    is_admin: Optional[bool]
    is_superuser: bool
    date_joined: Optional[datetime]
