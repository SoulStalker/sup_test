from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.forms import ModelForm
from src.models.models import CustomUser, CustomUserList, Permission, Role


class CustomUserForm(ModelForm):
    """Форма модели CustomUser."""

    password = ReadOnlyPasswordHashField(
        label="пароль",
        help_text="Пароли не хранятся в открытом виде, поэтому мы не можем показать вам пароль, но вы можете изменить его.",
    )

    class Meta:
        model = CustomUser
        fields = [
            "name",
            "surname",
            "password",
            "email",
            "tg_name",
            "tg_nickname",
            "google_meet_nickname",
            "gitlab_nickname",
            "github_nickname",
            "role",
            "avatar",
            "permissions",
        ]


class CustomUserListForm(ModelForm):
    """Форма для просмотра списка пользователей."""

    role = forms.ModelChoiceField(
        queryset=Role.objects.all(),
        required=False,
        label="Роль",
        help_text="Выберите роль пользователя",
    )
    user = forms.ModelChoiceField(
        queryset=CustomUser.objects.all(),
        required=True,
        label="Пользователь",
        help_text="Выберите пользователя",
    )

    class Meta:
        model = CustomUserList
        exclude = ["avatar", "permissions"]


class RoleForm(ModelForm):
    """Форма модели Role."""

    class Meta:
        model = Role
        fields = [
            "name",
            "color",
        ]


class PermissionsForm(ModelForm):
    """Форма модели Permissions."""

    class Meta:
        model = Permission
        fields = [
            "name",
            "code",
            "description",
        ]


class PasswordChangeForm(forms.Form):
    """Форма для изменения пароля."""

    current_password = forms.CharField(
        widget=forms.PasswordInput, label="текущий пароль"
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput, label="новый пароль"
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput, label="повторите новый пароль"
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        current_password = self.cleaned_data.get("current_password")
        if not self.user.check_password(current_password):
            raise forms.ValidationError("Текущий пароль введен неверно")
        return current_password

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get("new_password1")
        new_password2 = self.cleaned_data.get("new_password2")

        if new_password1 != new_password2:
            raise forms.ValidationError("Пароли не совпадают")

        if new_password1 == self.user.password:
            raise forms.ValidationError(
                "Новый пароль должен отличаться от старого"
            )

        return new_password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data["new_password2"])
        if commit:
            self.user.save()
        return self.user


class RegistrationForm(forms.Form):
    """Форма для Регистрации."""

    name = forms.CharField(
        widget=forms.TextInput, label="Имя",
        max_length=20,
    )
    surname = forms.CharField(
        widget=forms.TextInput, label="Фамилия",
        max_length=20,
    )
    email = forms.EmailField(
        widget=forms.EmailInput, label="E-mail",
        max_length=50,
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput, label="Пароль"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput, label="Повторите пароль"
    )
    tg_name = forms.CharField(
        widget=forms.TextInput, label="Имя в телеграмме",
        max_length=50,
    )
    tg_nickname = forms.CharField(
        widget=forms.TextInput, label="Ник в телеграмме",
        max_length=50,
    )
    google_meet_nickname = forms.CharField(
        widget=forms.TextInput, label="Ник в гугл мит",
        max_length=50,
    )
    gitlab_nickname = forms.CharField(
        widget=forms.TextInput, label="Ник в GitLab",
        max_length=50,
    )
    github_nickname = forms.CharField(
        widget=forms.TextInput, label="Ник в GitGub",
        max_length=50,
    )    