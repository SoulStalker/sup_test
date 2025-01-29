import secrets
import string
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.domain.base import Entity


@dataclass
class CreateUserEntity(Entity):
    name: str
    surname: str
    email: str
    password: Optional[str]
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

    @classmethod
    def generate_password(cls) -> str:
        # Определяем обязательные компоненты
        uppercase = secrets.choice(string.ascii_uppercase)  # Заглавная буква
        digit = secrets.choice(string.digits)  # Цифра
        special = secrets.choice("!@#$%^&*()-_=+[]{}|;:,.<>?/")  # Спецсимвол
        length = 8  # Минимальная длина пароля

        # Остальные символы (чтобы длина была >= 8)
        remaining_length = length - 3  # Уже есть три символа
        all_characters = (
            string.ascii_letters
            + string.digits
            + "!@#$%^&*()-_=+[]{}|;:,.<>?/"
        )
        remaining = "".join(
            secrets.choice(all_characters) for _ in range(remaining_length)
        )

        # Собираем пароль и перемешиваем символы
        password = uppercase + digit + special + remaining
        shuffled_password = "".join(
            secrets.choice(password) for _ in range(len(password))
        )

        return shuffled_password

    def verify_data(self):
        return super().verify_data(self.name)


@dataclass
class UserEntity(CreateUserEntity):
    id: int
    date_joined: datetime | None
    meet_statuses: dict[int:str] | None


@dataclass
class CreatePermissionEntity(Entity):
    name: str
    code: str
    description: str
    content_type: str
    object_id: int | None

    def verify_data(self):
        return super().verify_data(self.name)


@dataclass
class PermissionEntity(CreatePermissionEntity):
    id: int


@dataclass
class CreateRoleEntity(Entity):
    name: str
    color: str

    def verify_data(self):
        return super().verify_data(self.name)


@dataclass
class RoleEntity(CreateRoleEntity):
    id: int
