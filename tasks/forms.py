from . import models
from django import forms
from django.core.exceptions import ValidationError

class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = models.Task
        fields = ('title', 'desired_weekly_frequency',)
