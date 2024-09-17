from django.core.validators import MaxValueValidator, RegexValidator


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
