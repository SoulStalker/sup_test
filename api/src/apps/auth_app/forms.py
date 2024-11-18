from django import forms
from django.core.validators import RegexValidator


class LoginForm(forms.Form):
    email = forms.EmailField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Email"}),
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
                message="Недопустимый email.",
            )
        ],
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Пароль"}),
        # validators=[
        #     RegexValidator(
        #         regex=r"^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$",
        #         message="Пароль должен быть не менее 8 символов и содержать заглавную букву, цифру и спецсимвол.",
        #     )
        # ],
    )
