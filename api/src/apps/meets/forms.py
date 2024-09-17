from django import forms
from django.contrib.auth.models import User

from .models import Category


class CreateMeetForm(forms.Form):
    title = forms.CharField()
    start_date = forms.DateField()
    start_time = forms.TimeField()
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    author = User.objects.get(pk=1)
    responsible = forms.ModelChoiceField(queryset=User.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["participants"] = forms.MultipleChoiceField(
            choices=[(user.id, user.username) for user in User.objects.all()],
            widget=forms.CheckboxSelectMultiple,
            required=False,
        )

    def clean(self):
        cleaned_data = super().clean()
        participants = cleaned_data.get("participants", [])
        participant_statuses = {}

        for key, value in self.data.items():
            if key.startswith("participant_status_"):
                user_id = key.split("_")[-1]
                if user_id in participants:
                    participant_statuses[user_id] = value

        cleaned_data["participant_statuses"] = participant_statuses
        return cleaned_data
