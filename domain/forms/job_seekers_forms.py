from datetime import timedelta
from datetime import datetime as dt
from django import forms
from domain.models import *


class JobSeekerForm(forms.ModelForm):
    class Meta:
        model = JobSeeker
        fields = '__all__'
