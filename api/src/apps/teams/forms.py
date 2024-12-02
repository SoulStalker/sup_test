from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class CreateTeamForm(forms.Form):
    id = forms.IntegerField()
    name = forms.CharField()
    members_count = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["participants"] = forms.MultipleChoiceField(
            choices=[(user.id, user.name) for user in User.objects.all()],
            widget=forms.CheckboxSelectMultiple,
            required=False,
        )

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
