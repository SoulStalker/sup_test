from django import forms
from django.contrib.auth.models import User
from src.models.projects import Feature, Project, Task, Tags


class TagForm(forms.ModelForm):
    class Meta:
        model = Tags
        fields = ["name", "color"]


class FeatureForm(forms.ModelForm):
    class Meta:
        model = Feature
        fields = [
            "name",
            "responsible",
            "description",
            "tags",
            "participants",
            "importance",
            "status",
        ]


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'name',
            'logo',
            'description',
            'status',
            'participants',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["participants"] = forms.ModelMultipleChoiceField(
            queryset=User.objects.all(),
            widget=forms.CheckboxSelectMultiple
        )

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('participants') is None:
            cleaned_data['participants'] = []
        return cleaned_data


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "name",
            "feature",
            "description",
            "tags",
            "participants",
            "importance",
            "date_execution",
            "status",
        ]
