from typing import Optional, Tuple

from src.domain.base import BaseService

from .dtos import InviteDTO
from .entity import InviteEntity
from .repository import IInviteRepository


class InviteService(BaseService):
    """
    Сервис для работы с приглашениями.
    """

    def __init__(self, repository: IInviteRepository):
        """
        Инициализирует сервис с указанным репозиторием.

        :param repository: Репозиторий для работы с приглашениями.
        """
        self._repository = repository

    def create(
        self, user_id: int
    ) -> Tuple[Optional[InviteDTO], Optional[str]]:
        """
        Создает новое приглашение для указанного пользователя.

        :param user_id: Идентификатор пользователя.
        :return: Кортеж (DTO приглашения, ошибка), где DTO — созданное приглашение, а ошибка — сообщение об ошибке.
        """
        # Проверяем наличие прав
        if not self._repository.has_permission(user_id, 3):
            return None, "У вас нет прав на создание данного объекта"
        return self._repository.create(user_id)

    def create_invite_dto(self, invitation_code: str) -> Optional[InviteDTO]:
        """
        Создает DTO приглашения на основе кода приглашения.

        :param invitation_code: Код приглашения.
        :return: DTO приглашения или None, если приглашение не найдено.
        """
        return self._repository.create_invite_dto(invitation_code)

    def update_status(
        self, dto: InviteDTO, status: str = "EXPIRED"
    ) -> Optional[str]:
        """
        Обновляет статус приглашения.

        :param dto: DTO приглашения.
        :param status: Новый статус приглашения (по умолчанию "EXPIRED").
        :return: Сообщение об ошибке, если статус невалиден, иначе None.
        """
        invite = InviteEntity(
            pk=dto.id,
            link=dto.link,
            status=dto.status,
            created_at=dto.created_at,
            expires_at=dto.expires_at,
        )
        if status == "EXPIRED":
            status = invite.expire_status()
        elif status == "USED":
            status = invite.use_invite()
        else:
            return "Invalid status"
        self._repository.update_status(invite.pk, status)
        return None

    def has_permission(self, user_id: int, action: str, obj=None) -> bool:
        """
        Проверяет наличие прав у пользователя на выполнение действия над объектом.

        :param user_id: Идентификатор пользователя.
        :param action: Код действия.
        :param obj: Объект, над которым выполняется действие. Если None, проверяется глобальное разрешение.
        :return: True, если пользователь имеет права, иначе False.
        """
        return self._repository.has_permission(user_id, action, obj)
