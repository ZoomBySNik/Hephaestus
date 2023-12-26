from datetime import timedelta
from datetime import datetime as dt
from django import forms
from domain.models import *


class JobSeekerForm(forms.ModelForm):
    locality = forms.CharField(max_length=255, label='Населенный пункт',
                               error_messages={"required": "Введите населённый пункт"})
    class Meta:
        model = JobSeeker
        fields = '__all__'
        exclude = ['address', 'specialization', 'skill', 'about']
        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
            'about': forms.Textarea(attrs={'rows': 4}),
        }
