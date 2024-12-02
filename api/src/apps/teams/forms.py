from django import forms
from django.contrib.auth import get_user_model
from django.utils.functional import cached_property

User = get_user_model()


class CreateTeamForm(forms.Form):
    id = forms.IntegerField()
    name = forms.CharField()
    participants = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        label="Участники",
        widget=forms.CheckboxSelectMultiple,
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
