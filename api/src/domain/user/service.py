from typing import Dict, Optional, Tuple

from src.domain.base import BaseService
from src.domain.user.dtos import (
    CreatePermissionDTO,
    CreateRoleDTO,
    PermissionDTO,
    RoleDTO,
    UserDTO,
)
from src.domain.user.entity import CreatePermissionEntity, CreateUserEntity
from src.domain.user.repository import (
    IPermissionRepository,
    IRoleRepository,
    IUserRepository,
)


class RoleService(BaseService):
    """
    Сервис для работы с ролями.
    """

    def __init__(self, repository: IRoleRepository):
        """
        Инициализирует сервис с указанным репозиторием.

        :param repository: Репозиторий для работы с ролями.
        """
        self._repository = repository

    def create(
        self, dto: CreateRoleDTO, user_id: int
    ) -> Tuple[Optional[RoleDTO], Optional[str]]:
        """
        Создает новую роль.

        :param dto: DTO роли.
        :param user_id: Идентификатор пользователя.
        :return: Кортеж (DTO роли, ошибка), где DTO — созданная роль, а ошибка — сообщение об ошибке.
        """
        entity = dto
        return self.validate_and_save(entity, self._repository, dto, user_id)

    def update(
        self, pk: int, dto: RoleDTO, user_id: int
    ) -> Tuple[Optional[RoleDTO], Optional[str]]:
        """
        Обновляет существующую роль.

        :param pk: Идентификатор роли.
        :param dto: DTO роли с обновленными данными.
        :param user_id: Идентификатор пользователя.
        :return: Кортеж (DTO роли, ошибка), где DTO — обновленная роль, а ошибка — сообщение об ошибке.
        """
        entity = dto
        return self.validate_and_update(
            entity, self._repository, dto, pk, user_id
        )

    def get_roles_participants_count(self, role_id: int) -> int:
        """
        Получает количество участников с определенной ролью.

        :param role_id: Идентификатор роли.
        :return: Количество участников.
        """
        return self._repository.get_roles_participants_count(role_id)


class PermissionService(BaseService):
    """
    Сервис для работы с разрешениями.
    """

    def __init__(self, repository: IPermissionRepository):
        """
        Инициализирует сервис с указанным репозиторием.

        :param repository: Репозиторий для работы с разрешениями.
        """
        self._repository = repository

    def create(
        self, dto: CreatePermissionDTO, user_id: int
    ) -> Tuple[Optional[PermissionDTO], Optional[str]]:
        """
        Создает новое разрешение.

        :param dto: DTO разрешения.
        :param user_id: Идентификатор пользователя.
        :return: Кортеж (DTO разрешения, ошибка), где DTO — созданное разрешение, а ошибка — сообщение об ошибке.
        """
        entity = CreatePermissionEntity(
            name=dto.name,
            code=dto.code,
            description=dto.description,
            content_type=dto.content_type,
            object_id=dto.object_id,
        )
        return self.validate_and_save(entity, self._repository, dto, user_id)

    def update(
        self, pk: int, dto: PermissionDTO, user_id: int
    ) -> Tuple[Optional[PermissionDTO], Optional[str]]:
        """
        Обновляет существующее разрешение.

        :param pk: Идентификатор разрешения.
        :param dto: DTO разрешения с обновленными данными.
        :param user_id: Идентификатор пользователя.
        :return: Кортеж (DTO разрешения, ошибка), где DTO — обновленное разрешение, а ошибка — сообщение об ошибке.
        """
        entity = dto
        return self.validate_and_update(
            entity, self._repository, dto, pk, user_id
        )

    def get_content_types(self) -> list[str]:
        """
        Получает список типов контента.

        :return: Список типов контента.
        """
        return self._repository.get_content_types()

    def get_content_object(self, permission_id: int) -> Optional[Dict]:
        """
        Получает объект контента по идентификатору разрешения.

        :param permission_id: Идентификатор разрешения.
        :return: Объект контента или None, если объект не найден.
        """
        return self._repository.get_content_object(permission_id)

    def get_content_objects(self) -> list[Dict]:
        """
        Получает список объектов контента.

        :return: Список объектов контента.
        """
        return self._repository.get_content_objects()

    def get_codes(self) -> list[str]:
        """
        Получает список кодов разрешений.

        :return: Список кодов разрешений.
        """
        return self._repository.get_codes()

    def get_objects_data(self, content_type_id: int) -> list[Dict]:
        """
        Получает данные объектов по типу контента.

        :param content_type_id: Идентификатор типа контента.
        :return: Список данных объектов.
        """
        return self._repository.get_objects_data(content_type_id)


class UserService(BaseService):
    """
    Сервис для работы с пользователями.
    """

    def __init__(self, repository: IUserRepository):
        """
        Инициализирует сервис с указанным репозиторием.

        :param repository: Репозиторий для работы с пользователями.
        """
        self._repository = repository

    def create(
        self, dto: CreateUserEntity, user_id: int
    ) -> Tuple[Optional[UserDTO], Optional[str]]:
        """
        Создает нового пользователя.

        :param dto: Сущность пользователя.
        :param user_id: Идентификатор пользователя.
        :return: Кортеж (DTO пользователя, ошибка), где DTO — созданный пользователь, а ошибка — сообщение об ошибке.
        """
        entity = dto
        return self.validate_and_save(entity, self._repository, dto, user_id)

    def update(
        self, pk: int, dto: UserDTO, user_id: int
    ) -> Tuple[Optional[UserDTO], Optional[str]]:
        """
        Обновляет существующего пользователя.

        :param pk: Идентификатор пользователя.
        :param dto: DTO пользователя с обновленными данными.
        :param user_id: Идентификатор пользователя.
        :return: Кортеж (DTO пользователя, ошибка), где DTO — обновленный пользователь, а ошибка — сообщение об ошибке.
        """
        entity = dto
        return self.validate_and_update(
            entity, self._repository, dto, pk, user_id
        )

    def change_password(self, user_id: int, new_password: str) -> None:
        """
        Изменяет пароль пользователя.

        :param user_id: Идентификатор пользователя.
        :param new_password: Новый пароль.
        """
        user = self._repository.get_by_id(user_id)
        user.set_password(new_password)
        user.save()

    def create_user_with_generated_password(self, dto: UserDTO) -> UserDTO:
        """
        Создает пользователя с автоматически сгенерированным паролем.

        :param dto: DTO пользователя.
        :return: Созданный DTO пользователя.
        """
        password = self.generate_password()
        user = self._repository.create(dto)
        user.set_password(password)
        user.save()
        return user

    def send_welcome_email(self, user_dto: UserDTO) -> None:
        """
        Отправляет приветственное письмо пользователю.

        :param user_dto: DTO пользователя.
        """
        self._repository.send_welcome_email(user_dto)

    def get_user_id_list(self, user_list_id: list[int]) -> list[int]:
        """
        Получает список идентификаторов пользователей.

        :param user_list_id: Список идентификаторов пользователей.
        :return: Список идентификаторов пользователей.
        """
        return self._repository.get_user_id_list(user_list_id)
