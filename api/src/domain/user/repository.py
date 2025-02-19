from abc import abstractmethod
from typing import Dict, Optional, Tuple

from src.domain.base import BaseRepository
from src.domain.user.dtos import CreateRoleDTO, PermissionDTO, RoleDTO, UserDTO
from src.domain.user.entity import CreatePermissionEntity, CreateUserEntity


class IRoleRepository(BaseRepository):
    """
    Интерфейс репозитория для работы с ролями.
    """

    @abstractmethod
    def create(
        self, dto: CreateRoleDTO
    ) -> Tuple[Optional[RoleDTO], Optional[str]]:
        """
        Создает новую роль.

        :param dto: DTO роли.
        :return: Кортеж (DTO роли, ошибка), где DTO — созданная роль, а ошибка — сообщение об ошибке.
        """
        raise NotImplementedError

    @abstractmethod
    def update(
        self, role_id: int, dto: RoleDTO
    ) -> Tuple[Optional[RoleDTO], Optional[str]]:
        """
        Обновляет данные роли.

        :param role_id: Идентификатор роли.
        :param dto: DTO роли с обновленными данными.
        :return: Кортеж (DTO роли, ошибка), где DTO — обновленная роль, а ошибка — сообщение об ошибке.
        """
        raise NotImplementedError

    @abstractmethod
    def get_roles_participants_count(self, role_id: int) -> int:
        """
        Получает количество участников с определенной ролью.

        :param role_id: Идентификатор роли.
        :return: Количество участников.
        """
        raise NotImplementedError


class IPermissionRepository(BaseRepository):
    """
    Интерфейс репозитория для работы с разрешениями.
    """

    @abstractmethod
    def create(
        self, dto: CreatePermissionEntity
    ) -> Tuple[Optional[PermissionDTO], Optional[str]]:
        """
        Создает новое разрешение.

        :param dto: Сущность разрешения.
        :return: Кортеж (DTO разрешения, ошибка), где DTO — созданное разрешение, а ошибка — сообщение об ошибке.
        """
        raise NotImplementedError

    @abstractmethod
    def update(
        self, permission_id: int, dto: PermissionDTO
    ) -> Tuple[Optional[PermissionDTO], Optional[str]]:
        """
        Обновляет данные разрешения.

        :param permission_id: Идентификатор разрешения.
        :param dto: DTO разрешения с обновленными данными.
        :return: Кортеж (DTO разрешения, ошибка), где DTO — обновленное разрешение, а ошибка — сообщение об ошибке.
        """
        raise NotImplementedError

    @abstractmethod
    def get_permission_by_code(self, code: str) -> Optional[PermissionDTO]:
        """
        Получает разрешение по его коду.

        :param code: Код разрешения.
        :return: DTO разрешения или None, если разрешение не найдено.
        """
        raise NotImplementedError

    @abstractmethod
    def get_content_types(self) -> list[str]:
        """
        Получает список типов контента.

        :return: Список типов контента.
        """
        raise NotImplementedError

    @abstractmethod
    def get_content_object(self, permission_id: int) -> Optional[Dict]:
        """
        Получает объект контента по идентификатору разрешения.

        :param permission_id: Идентификатор разрешения.
        :return: Объект контента или None, если объект не найден.
        """
        raise NotImplementedError

    @abstractmethod
    def get_content_objects(self) -> list[Dict]:
        """
        Получает список объектов контента.

        :return: Список объектов контента.
        """
        raise NotImplementedError

    @abstractmethod
    def get_codes(self) -> list[str]:
        """
        Получает список кодов разрешений.

        :return: Список кодов разрешений.
        """
        raise NotImplementedError

    @abstractmethod
    def get_objects_data(self, content_type_id: int) -> list[Dict]:
        """
        Получает данные объектов по типу контента.

        :param content_type_id: Идентификатор типа контента.
        :return: Список данных объектов.
        """
        raise NotImplementedError


class IUserRepository(BaseRepository):
    """
    Интерфейс репозитория для работы с пользователями.
    """

    @abstractmethod
    def create(
        self, dto: CreateUserEntity
    ) -> Tuple[Optional[UserDTO], Optional[str]]:
        """
        Создает нового пользователя.

        :param dto: Сущность пользователя.
        :return: Кортеж (DTO пользователя, ошибка), где DTO — созданный пользователь, а ошибка — сообщение об ошибке.
        """
        raise NotImplementedError

    @abstractmethod
    def update(
        self, user_id: int, dto: UserDTO
    ) -> Tuple[Optional[UserDTO], Optional[str]]:
        """
        Обновляет данные пользователя.

        :param user_id: Идентификатор пользователя.
        :param dto: DTO пользователя с обновленными данными.
        :return: Кортеж (DTO пользователя, ошибка), где DTO — обновленный пользователь, а ошибка — сообщение об ошибке.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, user_id: int) -> Optional[str]:
        """
        Удаляет пользователя.

        :param user_id: Идентификатор пользователя.
        :return: Сообщение об ошибке, если удаление не удалось, иначе None.
        """
        raise NotImplementedError

    @abstractmethod
    def send_welcome_email(self, user_dto: UserDTO) -> None:
        """
        Отправляет приветственное письмо пользователю.

        :param user_dto: DTO пользователя.
        """
        raise NotImplementedError

    @abstractmethod
    def get_active_users(self) -> list[UserDTO]:
        raise NotImplementedError
