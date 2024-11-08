import re
from django.core.validators import MaxValueValidator, RegexValidator, FileExtensionValidator
from django.core.exceptions import ValidationError

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
            "hex_color": r"^\d{6}$"  # 6 цифр для цвета
        }

    @staticmethod
    def verify_letters_only(value):
        """
        Проверяет строку на наличие только букв латиницы и кириллицы.
        """
        if not re.match(DataVerifier._get_regex_patterns()["letters_only"], value):
            return "Допускаются только буквы латиницы и кириллицы"
        return None

    @staticmethod
    def verify_letters_space_only(value):
        """
        Проверяет строку на наличие только букв латиницы и кириллицы и пробелов.
        """
        if not re.match(DataVerifier._get_regex_patterns()["letters_space_only"], value):
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
    def verify_letter_digits_symbols(value):
        """
        Проверяет строку на наличие только букв, цифр и спецсимволов.
        """
        if not re.match(DataVerifier._get_regex_patterns()["letters_digits_symbols"], value):
            return "Допускаются только буквы, цифры и спецсимволы"
        return None

    @staticmethod
    def verify_color(value):
        """
        Проверяет, является ли строка шестизначным числом (например, цвет в формате HEX).
        """
        if not re.match(DataVerifier._get_regex_patterns()["hex_color"], value):
            return "Цвет должен состоять из 6 цифр"
        return None

    @staticmethod
    def validate_file_extension(value):
        """
            Проверяет, является ли файл jpeg, png, 2Mb.
            """
        # Проверка на разрешение
        file_extension_validator = FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"])
        file_extension_validator(value)  # Вызов валидатора расширения

        # Проверка на размер
        max_size = 2 * 1024 * 1024  # 2 MB
        if value.size > max_size:
            raise ValidationError("Размер файла не должен превышать 2MB.")

class ModelValidator:
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
            "hex_color": r"^\d{6}$"  # 6 цифр для цвета
        }

    @staticmethod
    def validate_letters_only():
        """
        Валидатор, проверяющий наличие только букв латиницы и кириллицы.
        """
        return RegexValidator(
            regex=ModelValidator._get_regex_patterns()["letters_only"],
            message="Допускаются только буквы латиницы и кириллицы",
            code="invalid_name"
        )

    @staticmethod
    def validate_letters_space_only():
        """
        Валидатор, проверяющий наличие только букв и пробелов.
        """
        return RegexValidator(
            regex=ModelValidator._get_regex_patterns()["letters_space_only"],
            message="Допускаются только буквы и пробел"
        )

    @staticmethod
    def validate_max_value(limit_value=1_000_000):
        """
        Валидатор для максимального значения.
        """
        return MaxValueValidator(limit_value=limit_value)

    @staticmethod
    def validate_email():
        """
        Валидатор, проверяющий валидность email.
        """
        return RegexValidator(
            regex=ModelValidator._get_regex_patterns()["email"],
            message="Неверный формат email",
            code="invalid_email"
        )

    @staticmethod
    def validate_letter_digits_symbols():
        """
        Валидатор, проверяющий наличие только букв, цифр и спец. символов.
        """
        return RegexValidator(
            regex=ModelValidator._get_regex_patterns()["letters_digits_symbols"],
            message="Допускаются только буквы, цифры и спец.символы",
            code="invalid_name"
        )

    @staticmethod
    def validate_color():
        """
        Валидатор, проверяющий шестизначный код цвета (HEX).
        """
        return RegexValidator(
            regex=ModelValidator._get_regex_patterns()["hex_color"],
            message="Цвет должен состоять из 6 цифр.",
            code="invalid_color"
        )


