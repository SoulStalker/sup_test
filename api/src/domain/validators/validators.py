import re

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator


class DataVerifier:
    @staticmethod
    def _get_regex_patterns():
        """
        Возвращает словарь с регулярными выражениями для различных типов проверок.
        """
        return {
            "letters_only": r"^[a-zA-Zа-яА-Я\s]*$",  # Только буквы (латиница и кириллица)
            "letters_space_only": r"^[а-яА-ЯёЁa-zA-Z]+(?:\s[а-яА-ЯёЁa-zA-Z]+)*$",  # Буквы и пробелы
            "email": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",  # Email
            "letters_digits_symbols": r"^[a-zA-Zа-яА-Я0-9._%+-]+$",  # Буквы, цифры и спец. символы
            "hex_color": r"^([A-Fa-f0-9]{6})$",  # 6 цифр для цвета
        }

    @staticmethod
    def verify_letters_only(value: str) -> str | None:
        """
        Проверяет строку на наличие только букв латиницы и кириллицы.
        """
        if not re.match(
            DataVerifier._get_regex_patterns()["letters_only"], value
        ):
            return "Допускаются только буквы латиницы и кириллицы"
        return None

    @staticmethod
    def verify_letters_space_only(value: str) -> str | None:
        """
        Проверяет строку на наличие только букв латиницы и кириллицы и пробелов.
        """
        if not re.match(
            DataVerifier._get_regex_patterns()["letters_space_only"], value
        ):
            return "Допускаются только буквы и пробел"
        return None

    @staticmethod
    def verify_max_value(value, limit_value=1_000_000):
        """
        Проверяет значение на максимальное значение.
        """
        if len(value) > limit_value:
            return f"Максимальное допустимое значение: {limit_value} символов"
        return None

    @staticmethod
    def verify_email(value):
        """
        Проверяет строку на наличие валидного email-адреса.
        """
        if not re.match(DataVerifier._get_regex_patterns()["email"], value):
            return "Неверный формат email"
        return None

    @staticmethod
    def verify_letter_digits_symbols(value: str) -> str | None:
        """
        Проверяет строку на наличие только букв, цифр и спецсимволов.
        """
        if not re.match(
            DataVerifier._get_regex_patterns()["letters_digits_symbols"], value
        ):
            return "Допускаются только буквы, цифры и спецсимволы"
        return None

    @staticmethod
    def verify_color(value):
        """
        Проверяет, является ли строка шестизначным числом (например, цвет в формате HEX).
        """
        if not re.match(
            DataVerifier._get_regex_patterns()["hex_color"], value
        ):
            return "Цвет должен быть в формате RRGGBB"
        return None

    @staticmethod
    def validate_file_extension(value: object) -> None:
        """
        Проверяет, является ли файл jpeg, png, 2Mb.
        """
        # Проверка на разрешение
        file_extension_validator = FileExtensionValidator(
            allowed_extensions=["jpg", "jpeg", "png"]
        )
        file_extension_validator(value)  # Вызов валидатора расширения

        # Проверка на размер
        max_size = 2 * 1024 * 1024  # 2 MB
        if value.size > max_size:
            raise ValidationError("Размер файла не должен превышать 2MB.")

    @staticmethod
    def verify_password_eq(password1: str, password2: str) -> str | None:
        """
        Проверяет одинаковы ли пароли.
        """
        if password1 != password2:
            return "Пароли не совпадают"
        return None

    @staticmethod
    def clean_password(password: str) -> str | None:
        if len(password) < 8:
            return "Пароль должен содержать не менее 8 символов."
        elif not re.search(r"[A-Z]", password):
            return "Пароль должен содержать хотя бы одну заглавную букву."
        elif not re.search(r"[a-z]", password):
            return "Пароль должен содержать хотя бы одну строчную букву."
        elif not re.search(r"[0-9]", password):
            return "Пароль должен содержать хотя бы одну цифру."
        elif not re.search(r"[\W_]", password):
            return "Пароль должен содержать хотя бы один специальный символ."
        return None

    @staticmethod
    def validate_letters_space_only(value):
        """
        Валидатор, который проверяет, содержит ли строка только буквы и пробелы.
        """
        # Проверяем, что строка состоит только из букв и пробелов
        if not re.match("^[A-Za-zА-Яа-яЁё\s]+$", value):
            raise ValidationError(
                "Название должно содержать только буквы и пробелы.",
                code="invalid_characters",
            )