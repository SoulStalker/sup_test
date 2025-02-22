from django import forms
from django.contrib.auth import get_user_model
from django.utils.functional import cached_property
from src.domain.validators import DataVerifier
from src.models.choice_classes import (
    FeaturesChoices,
    ProjectChoices,
    TaskChoices,
)
from src.models.projects import Features, Project, Tags

User = get_user_model()


class ProjectForm(forms.Form):
    name = forms.CharField(
        max_length=20,
        label="Название",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        validators=[DataVerifier.validate_letters_space_only],
    )

    logo = forms.ImageField(
        label="Логотип",
        widget=forms.FileInput(attrs={"class": "form-control"}),
        validators=[DataVerifier.validate_file_extension],
        required=False,
    )

    description = forms.CharField(
        max_length=10000,
        label="Описание",
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 5}),
    )

    status = forms.ChoiceField(
        choices=ProjectChoices.choices,
        label="Статус",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    participants = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        label="Участники",
        widget=forms.CheckboxSelectMultiple,
    )

    date_created = forms.DateTimeField(
        label="Дата создания",
        widget=forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
    )

    responsible = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Ответственный",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["participants"] = forms.ModelMultipleChoiceField(
            queryset=self.users_queryset, widget=forms.CheckboxSelectMultiple
        )

    @cached_property
    def users_queryset(self):
        """Возвращает активных пользователей для выбора в форме."""
        return User.objects.filter(is_active=True)

    def clean(self):
        """Очистка данных формы."""
        cleaned_data = super().clean()
        if cleaned_data.get("participants") is None:
            cleaned_data["participants"] = []
        return cleaned_data


class CreateFeaturesForm(forms.Form):

    name = forms.CharField(
        max_length=20,
        label="Название",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        validators=[DataVerifier.validate_letters_space_only],
    )

    description = forms.CharField(
        max_length=10000,
        label="Описание",
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 5}),
    )

    responsible = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Ответственный",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    tags = forms.ModelMultipleChoiceField(
        queryset=Tags.objects.all(),
        label="Теги",
        widget=forms.CheckboxSelectMultiple,
    )

    participants = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        label="Участники",
        widget=forms.CheckboxSelectMultiple,
    )

    importance = forms.IntegerField(
        label="Важность",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )

    status = forms.ChoiceField(
        choices=FeaturesChoices.choices,
        label="Статус",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    project = forms.ModelChoiceField(
        label="Проект",
        queryset=Project.objects.all(),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["participants"] = forms.ModelMultipleChoiceField(
            queryset=self.users_queryset, widget=forms.CheckboxSelectMultiple
        )

    @cached_property
    def users_queryset(self):
        """Возвращает активных пользователей для выбора в форме."""
        return User.objects.filter(is_active=True)

    def clean(self):
        """Очистка данных формы."""
        cleaned_data = super().clean()
        if cleaned_data.get("participants") is None:
            cleaned_data["participants"] = []
        return cleaned_data


class TaskForm(forms.Form):

    name = forms.CharField(
        max_length=20,
        label="Название",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        validators=[DataVerifier.validate_letters_space_only],
    )

    priority = forms.IntegerField(
        label="Приоритет",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )

    tags = forms.ModelMultipleChoiceField(
        queryset=Tags.objects.all(),
        label="Теги",
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    contributor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Исполнитель",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    responsible = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Ответственный",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    status = forms.ChoiceField(
        choices=TaskChoices.choices,
        label="Статус",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    closed_at = forms.DateField(
        label="Дата закрытия",
        widget=forms.DateInput(attrs={"class": "form-control"}),
        required=False,
    )

    feature = forms.ModelChoiceField(
        queryset=Features.objects.all(),
        label="Фича",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    description = forms.CharField(
        max_length=10000,
        label="Описание",
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 5}),
    )


class CommentForm(forms.Form):
    comment = forms.CharField(
        max_length=1000,
        label="Коментарий",
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 5}),
    )
