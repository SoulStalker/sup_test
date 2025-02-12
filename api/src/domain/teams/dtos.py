from dataclasses import dataclass
from typing import Optional

from src.domain.validators.validators import DataVerifier


@dataclass
class CreateTeamDTO:
    """
    DTO для создания команды.

    :param name: Название команды.
    :param participants: Список идентификаторов участников команды.
    """

    name: str
    participants: list[int]

    def verify_data(self) -> Optional[str]:
        """
        Проверяет валидность данных команды.

        :return: Сообщение об ошибке, если данные невалидны, иначе None.
        """
        letters_error = DataVerifier.verify_letters_space_only(self.name)
        len_error = DataVerifier.verify_max_value(self.name, 20)
        if letters_error:
            return letters_error
        elif len_error:
            return len_error
        return None


@dataclass
class TeamDTO(CreateTeamDTO):
    """
    DTO для команды.

    :param id: Уникальный идентификатор команды.
    """

    id: int
