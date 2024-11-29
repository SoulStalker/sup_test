from django.core.validators import MaxValueValidator, RegexValidator


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
            "hex_color": r"^([A-Fa-f0-9]{6})$",
            "password": r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$",  # пароль
        }

    @staticmethod
    def validate_letters_only():
        """
        Валидатор, проверяющий наличие только букв латиницы и кириллицы.
        """
        return RegexValidator(
            regex=ModelValidator._get_regex_patterns()["letters_only"],
            message="Допускаются только буквы латиницы и кириллицы",
            code="invalid_name",
        )

    @staticmethod
    def validate_letters_space_only():
        """
        Валидатор, проверяющий наличие только букв и пробелов.
        """
        return RegexValidator(
            regex=ModelValidator._get_regex_patterns()["letters_space_only"],
            message="Допускаются только буквы и пробел",
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
            code="invalid_email",
        )

    @staticmethod
    def validate_letter_digits_symbols():
        """
        Валидатор, проверяющий наличие только букв, цифр и спец. символов.
        """
        return RegexValidator(
            regex=ModelValidator._get_regex_patterns()[
                "letters_digits_symbols"
            ],
            message="Допускаются только буквы, цифры и спец.символы",
            code="invalid_name",
        )

    @staticmethod
    def validate_color():
        """
        Валидатор, проверяющий шестизначный код цвета (HEX).
        """
        return RegexValidator(
            regex=ModelValidator._get_regex_patterns()["hex_color"],
            message="Цвет должен быть в формате RRGGBB",
            code="invalid_color",
        )

    @staticmethod
    def validate_password():
        """
        Валидатор, проверяющий пароль.
        """
        return RegexValidator(
            regex=ModelValidator._get_regex_patterns()["password"],
            message="Пароль должен содержать строчные и заглавные буквы и цифры",
            code="invalid_password",
        )
