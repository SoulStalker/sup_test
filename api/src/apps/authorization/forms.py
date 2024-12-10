from django import forms


class AuthorizationForm(forms.Form):
    """Форма для авторизации."""

    email = forms.EmailField(
        widget=forms.EmailInput,
        label="E-mail",
        max_length=50,
    )
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")