from django import forms
from django.contrib.auth import get_user_model
from src.models.meets import Category

User = get_user_model()


class CreateMeetForm(forms.Form):
    title = forms.CharField()
    start_time = forms.DateTimeField()
    category = forms.ModelChoiceField(queryset=Category.objects.all())
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
