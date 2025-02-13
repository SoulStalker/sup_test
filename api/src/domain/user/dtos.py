from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional


@dataclass
class CreateRoleDTO:
    """
    DTO для создания роли.

    :param name: Название роли.
    :param color: Цвет роли.
    """

    name: str
    color: str


@dataclass
class RoleDTO(CreateRoleDTO):
    """
    DTO для роли.

    :param id: Уникальный идентификатор роли.
    """

    id: int


@dataclass
class CreatePermissionDTO:
    """
    DTO для создания разрешения.

    :param name: Название разрешения.
    :param code: Код разрешения.
    :param description: Описание разрешения.
    :param content_type: Тип контента, к которому применяется разрешение.
    :param object_id: Идентификатор объекта, к которому применяется разрешение (опционально).
    """

    name: str
    code: str
    description: str
    content_type: str
    object_id: Optional[int]


@dataclass
class PermissionDTO(CreatePermissionDTO):
    """
    DTO для разрешения.

    :param id: Уникальный идентификатор разрешения.
    """

    id: int


@dataclass
class UserDTO:
    """
    DTO для пользователя.

    :param id: Уникальный идентификатор пользователя.
    :param name: Имя пользователя.
    :param surname: Фамилия пользователя.
    :param email: Электронная почта пользователя.
    :param tg_name: Имя пользователя в Telegram.
    :param tg_nickname: Никнейм пользователя в Telegram.
    :param google_meet_nickname: Никнейм пользователя в Google Meet.
    :param gitlab_nickname: Никнейм пользователя в GitLab.
    :param github_nickname: Никнейм пользователя в GitHub.
    :param avatar: Аватар пользователя (опционально).
    :param role_id: Идентификатор роли пользователя.
    :param team_id: Идентификатор команды пользователя (опционально).
    :param permissions_ids: Список идентификаторов разрешений пользователя.
    :param is_active: Флаг активности пользователя (опционально).
    :param is_admin: Флаг администратора пользователя (опционально).
    :param is_superuser: Флаг суперпользователя пользователя (опционально).
    :param date_joined: Дата и время регистрации пользователя (опционально).
    :param meet_statuses: Статусы пользователя в митингах (опционально).
    """

    id: int
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
    is_superuser: Optional[bool]
    date_joined: Optional[datetime]
    meet_statuses: Optional[Dict[int, str]]
