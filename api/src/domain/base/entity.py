from dataclasses import dataclass

from src.domain.validators.validators import DataVerifier


@dataclass
class Entity:

    def verify_data(self, field: str) -> str:
        """
        Проверка валидности
        """
        letters_error = DataVerifier.verify_letters_space_only(field)
        len_error = DataVerifier.verify_max_value(field, 20)
        if letters_error:
            return letters_error
        elif len_error:
            return len_error
        return ""
