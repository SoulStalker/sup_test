import re
from django.core.validators import MaxValueValidator, RegexValidator


class LettersOnlyVerifier:
    @staticmethod
    def verify(value):
        """
        Проверяет строку на наличие только букв латиницы и кириллицы.
        Args:
            value: Строка для проверки.
        Returns:
            None, если строка действительна.
            Возвращает строку ошибки, если строка недействительна.
        """
        if not re.match(r"^[a-zA-Zа-яА-Я\s]*$", value):
            return "Допускаются только буквы латиницы и кириллицы."
        return None

    @staticmethod
    def verify_max_value(value, limit_value=1_000_000):
        """
        Проверяет значение на максимальное значение.
        Args:
            value: Значение для проверки.
            limit_value: Максимальное допустимое значение.
        Returns:
            None, если значение меньше или равно limit_value.
            Возвращает строку ошибки, если значение больше limit_value.
        """
        if value > limit_value:
            return f"Максимальное допустимое значение: {limit_value}."
        return None


class LettersOnlyValidator:
    @staticmethod
    def get_regex_validator():
        return RegexValidator(
            regex=r"^[a-zA-Zа-яА-Я\s]*$",
            message="Допускаются только буквы латиницы и кириллицы.",
            code="invalid_name",
        )

    @staticmethod
    def get_max_value_validator():
        return MaxValueValidator(limit_value=1_000_000)


class CustomValidator:
    @staticmethod
    def get_regex_validator():
        return RegexValidator(
            regex=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            message="Допускаются буквы латиницы, цифры и спец. символы. Не допускается пробел.",
            code="invalid_name",
        )


class LettersAndSymbolsValidator:
    @staticmethod
    def get_regex_validator():
        return RegexValidator(
            regex=r"^[a-zA-Zа-яА-Я0-9._%+-]+$",
            message="Допускаются только буквы, цифры и спец.символы.",
            code="invalid_name",
        )


class ColorValidator:
    @staticmethod
    def get_regex_validator():
        return RegexValidator(
            regex=r"^/d{6}$",
            message="Цвет должен состоять из 6 цифр.",
            code="invalid_color",
        )
