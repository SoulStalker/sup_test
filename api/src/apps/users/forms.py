from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.forms import ModelForm
from src.models.models import CustomUser, CustomUserList, Permission, Role


class CreateUserForm(forms.Form):
    """Форма для создания пользователя."""

    password = ReadOnlyPasswordHashField(
        label="пароль",
        help_text="Пароли не хранятся в открытом виде, поэтому мы не можем показать вам пароль, но вы можете изменить его.",
    )

    name = forms.CharField(max_length=30)
    surname = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)
    tg_name = forms.CharField(max_length=30, required=False)
    tg_nickname = forms.CharField(max_length=30, required=False)
    google_meet_nickname = forms.CharField(max_length=30, required=False)
    gitlab_nickname = forms.CharField(max_length=30, required=False)
    github_nickname = forms.CharField(max_length=30, required=False)
    role = forms.ModelChoiceField(
        queryset=Role.objects.all(),
        label="Роль",
        help_text="Выберите роль пользователя",
    )
    avatar = forms.ImageField(required=False)
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    is_active = forms.BooleanField(required=False)
    is_admin = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["permissions"].queryset = Permission.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("permissions") is None:
            cleaned_data["permissions"] = []
        return cleaned_data


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
