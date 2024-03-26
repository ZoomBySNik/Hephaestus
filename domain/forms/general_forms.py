from django import forms
from django.contrib.auth.forms import UserCreationForm

from domain.models import *


class EmployerRegistrationForm(UserCreationForm):
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'type': 'tel'}))
    class Meta:
        model = Employer
        fields = ['username', 'email', 'last_name', 'first_name',  'patronymic', 'phone_number']


class JobSeekerRegistrationForm(UserCreationForm):
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'type': 'tel'}))
    class Meta:
        model = JobSeeker
        fields = ['username', 'email', 'last_name', 'first_name', 'patronymic', 'phone_number']


class PhotoSaveForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_photo']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.profile_photo = self.cleaned_data['profile_photo']

        if commit:
            user.save()
        return user