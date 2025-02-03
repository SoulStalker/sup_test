from src.domain.base import BaseService

from .dtos import InviteDTO
from .entity import InviteEntity
from .repository import IInviteRepository


class InviteService(BaseService):
    def __init__(self, repository: IInviteRepository):
        self._repository = repository

    def create(self, user_id: int):
        # Проверяем наличие прав
        if not self._repository.has_permission(user_id, 3):
            return None, "У вас нет прав на создание данного объекта"
        return self._repository.create(user_id)

    def create_inviteDTO(self, invitation_code):
        return self._repository.create_inviteDTO(invitation_code)

    def update_status(self, dto: InviteDTO, status: str = "EXPIRED"):
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

    def has_permission(self, user_id: int, action: str, obj=None) -> bool:
        """
        Проверка наличия разрешения у пользователя.
        - action: код действия, например, "EDIT_TASK".
        - obj: объект, для которого проверяется разрешение. Если None, проверяется глобальное разрешение.
        """
        return self.has_permission(user_id, action, obj)
