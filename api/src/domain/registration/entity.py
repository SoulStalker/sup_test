import secrets
import string
from dataclasses import dataclass
from src.domain.validators.validators import DataVerifier



@dataclass
class RegistationEntity:
    name: str
    surname: str
    email: str
    password1: str
    password2: str
    tg_name: str
    tg_nickname: str
    google_meet_nickname: str
    gitlab_nickname: str
    github_nickname: str


    def verify_data(self):
        """
        Проверка валидности
        """
        password_eq_error = DataVerifier.verify_password_eq(self.password1, self.password2)
        if password_eq_error:
            return password_eq_error
        return None