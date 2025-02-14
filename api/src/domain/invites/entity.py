from dataclasses import dataclass
from datetime import datetime, timedelta

from src.domain.base import Entity
from src.models.choice_classes import InviteChoices


@dataclass
class InviteEntity(Entity):
    """
    Сущность приглашения, содержащая логику для работы с приглашениями.

    :param pk: Уникальный идентификатор приглашения.
    :param link: Ссылка на приглашение.
    :param status: Статус приглашения.
    :param created_at: Дата и время создания приглашения.
    :param expires_at: Дата и время истечения срока действия приглашения.
    """

    pk: int
    link: str
    status: str
    created_at: datetime
    expires_at: datetime

    def expire_status(self) -> str:
        """
        Обновляет статус приглашения на "EXPIRED", если оно истекло.

        :return: Новый статус приглашения.
        """
        if self.status == InviteChoices.ACTIVE and self.created_at.replace(
            tzinfo=None
        ) < datetime.now() - timedelta(days=7):
            self.status = InviteChoices.EXPIRED
        return self.status

    def use_invite(self) -> str:
        self.status = InviteChoices.USED
        return self.status
