from django import forms
from django.contrib.auth.models import User
from django.utils.functional import cached_property
from src.models.choice_classes import ProjectChoices


class ProjectForm(forms.Form):

    name = forms.CharField(
        max_length=50,
        label="Название",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    description = forms.CharField(
        max_length=10000,
        label="Описание",
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 5})
    )

    status = forms.ChoiceField(
        choices=ProjectChoices.choices,
        label="Статус",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    participants = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        label="Участники",
        widget=forms.CheckboxSelectMultiple
    )

    date_created = forms.DateField(
        label="Дата создания",
        widget=forms.DateInput(attrs={"class": "form-control"})
    )

    responsible = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Ответственный",
        widget=forms.Select(attrs={"class": "form-control"})
    )



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["participants"] = forms.ModelMultipleChoiceField(
            queryset=self.users_queryset,
            widget=forms.CheckboxSelectMultiple
        )

    @cached_property
    def users_queryset(self):
        """Возвращает активных пользователей для выбора в форме."""
        return User.objects.filter(is_active=True)

    def clean(self):
        """Очистка данных формы."""
        cleaned_data = super().clean()
        if cleaned_data.get('participants') is None:
            cleaned_data['participants'] = []
        return cleaned_data
