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


class SkillsForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(queryset=Skill.objects.all(),
                                           widget=forms.CheckboxSelectMultiple,
                                           label='Навыки')

    class Meta:
        model = JobSeeker
        fields = ('skills',)


class SpecializationForm(forms.ModelForm):
    specializations = forms.ModelMultipleChoiceField(queryset=Specialization.objects.all(),
                                           widget=forms.CheckboxSelectMultiple,
                                           label='Специализции')

    class Meta:
        model = JobSeeker
        fields = ('specializations',)


class SoftwareAndHardwareToolForm(forms.ModelForm):
    software_and_hardware_tools = forms.ModelMultipleChoiceField(queryset=SoftwareAndHardwareTool.objects.all(),
                                           widget=forms.CheckboxSelectMultiple,
                                           label='Программно-технические средства')

    class Meta:
        model = SoftwareAndHardwareToolOfJobSeeker
        fields = ('software_and_hardware_tools',)
