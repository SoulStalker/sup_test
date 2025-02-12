from dataclasses import dataclass
from typing import Optional

from src.domain.validators.validators import DataVerifier


@dataclass
class Entity:
    """
    Базовый класс для сущностей, предоставляющий методы для проверки валидности данных.
    """

    def verify_data(self, field: str) -> Optional[str]:
        """
        Проверяет валидность переданного поля.

        :param field: Поле для проверки.
        :return: Сообщение об ошибке, если поле невалидно, иначе None.
        """
        letters_error = DataVerifier.verify_letters_space_only(field)
        len_error = DataVerifier.verify_max_value(field, 20)
        if letters_error:
            return letters_error
        elif len_error:
            return len_error
        return None
