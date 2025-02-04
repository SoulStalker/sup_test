from django import forms


class RegistrationForm(forms.Form):
    """Форма для Регистрации."""

    name = forms.CharField(
        widget=forms.TextInput,
        label="Имя",
        max_length=20,
    )
    surname = forms.CharField(
        widget=forms.TextInput,
        label="Фамилия",
        max_length=20,
    )
    email = forms.EmailField(
        widget=forms.EmailInput,
        label="E-mail",
        max_length=50,
    )
    password1 = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    password2 = forms.CharField(
        widget=forms.PasswordInput, label="Повторите пароль"
    )
    tg_name = forms.CharField(
        widget=forms.TextInput,
        label="Имя в телеграмме",
        max_length=50,
    )
    tg_nickname = forms.CharField(
        widget=forms.TextInput,
        label="Ник в телеграмме",
        max_length=50,
    )
    google_meet_nickname = forms.CharField(
        widget=forms.TextInput,
        label="Ник в гугл мит",
        max_length=50,
    )
    gitlab_nickname = forms.CharField(
        widget=forms.TextInput,
        label="Ник в GitLab",
        max_length=50,
    )
    github_nickname = forms.CharField(
        widget=forms.TextInput,
        label="Ник в GitGub",
        max_length=50,
    )
