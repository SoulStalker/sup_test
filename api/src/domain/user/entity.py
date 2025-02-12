import secrets
import string
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional

from src.domain.base import Entity


@dataclass
class CreateUserEntity(Entity):
    """
    Сущность для создания пользователя.

    :param name: Имя пользователя.
    :param surname: Фамилия пользователя.
    :param email: Электронная почта пользователя.
    :param password: Пароль пользователя (опционально).
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
    :param is_superuser: Флаг суперпользователя пользователя.
    """

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
        """
        Генерирует случайный пароль.

        :return: Сгенерированный пароль.
        """
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

    def verify_data(self) -> Optional[str]:
        """
        Проверяет валидность данных пользователя.

        :return: Сообщение об ошибке, если данные невалидны, иначе None.
        """
        return super().verify_data(self.name)


@dataclass
class UserEntity(CreateUserEntity):
    """
    Сущность пользователя.

    :param id: Уникальный идентификатор пользователя.
    :param date_joined: Дата и время регистрации пользователя (опционально).
    :param meet_statuses: Статусы пользователя в митингах (опционально).
    """

    id: int
    date_joined: Optional[datetime]
    meet_statuses: Optional[Dict[int, str]]


@dataclass
class CreatePermissionEntity(Entity):
    """
    Сущность для создания разрешения.

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

    def verify_data(self) -> Optional[str]:
        """
        Проверяет валидность данных разрешения.

        :return: Сообщение об ошибке, если данные невалидны, иначе None.
        """
        return super().verify_data(self.name)


@dataclass
class PermissionEntity(CreatePermissionEntity):
    """
    Сущность разрешения.

    :param id: Уникальный идентификатор разрешения.
    """

    id: int


@dataclass
class CreateRoleEntity(Entity):
    """
    Сущность для создания роли.

    :param name: Название роли.
    :param color: Цвет роли.
    """

    name: str
    color: str

    def verify_data(self) -> Optional[str]:
        """
        Проверяет валидность данных роли.

        :return: Сообщение об ошибке, если данные невалидны, иначе None.
        """
        return super().verify_data(self.name)


@dataclass
class RoleEntity(CreateRoleEntity):
    """
    Сущность роли.

    :param id: Уникальный идентификатор роли.
    """

    id: int
