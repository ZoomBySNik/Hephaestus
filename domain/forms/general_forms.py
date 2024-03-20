from django import forms
from django.contrib.auth.forms import UserCreationForm

from domain.models import Employer, JobSeeker


class EmployerRegistrationForm(UserCreationForm):
    class Meta:
        model = Employer
        fields = ['username', 'email', 'last_name', 'first_name',  'patronymic', 'phone_number']


class JobSeekerRegistrationForm(UserCreationForm):
    class Meta:
        model = JobSeeker
        fields = ['username', 'email', 'last_name', 'first_name', 'patronymic', 'phone_number']
