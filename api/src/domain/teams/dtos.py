from dataclasses import dataclass

from src.domain.validators.validators import DataVerifier


@dataclass
class CreateTeamDTO:
    name: str
    participants: list[int]

    def verify_data(self):
        """
        Проверка валидности
        """
        letters_error = DataVerifier.verify_letters_space_only(self.name)
        len_error = DataVerifier.verify_max_value(self.name, 20)
        if letters_error:
            return letters_error
        elif len_error:
            return len_error


@dataclass
class TeamDTO(CreateTeamDTO):
    id: int
