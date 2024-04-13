from datetime import timedelta
from datetime import datetime as dt
from django import forms
from domain.models import *


class JobSeekerForm(forms.ModelForm):
    locality = forms.CharField(max_length=255, label='Населенный пункт', required=False)
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'type': 'tel'}), label='Номер телефона')

    class Meta:
        model = JobSeeker
        fields = ['last_name', 'first_name', 'patronymic', 'phone_number', 'email', 'birthdate', 'locality', 'about']
        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
        }


class SkillsForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(queryset=Skill.objects.all().order_by('name'),
                                            widget=forms.CheckboxSelectMultiple,
                                            label='Навыки')

    class Meta:
        model = JobSeeker
        fields = ('skills',)


class SpecializationForm(forms.ModelForm):
    specializations = forms.ModelMultipleChoiceField(queryset=Specialization.objects.all().order_by('name'),
                                                     widget=forms.CheckboxSelectMultiple,
                                                     label='Специализции')

    class Meta:
        model = JobSeeker
        fields = ('specializations',)


class SoftwareAndHardwareToolForm(forms.ModelForm):
    software_and_hardware_tools = forms.ModelMultipleChoiceField(queryset=SoftwareAndHardwareTool.objects.all().order_by('name'),
                                                                 widget=forms.CheckboxSelectMultiple,
                                                                 label='Программно-технические средства')

    class Meta:
        model = SoftwareAndHardwareToolOfJobSeeker
        fields = ('software_and_hardware_tools',)


class EducationForm(forms.ModelForm):
    education_organization_name = forms.CharField(max_length=255, label='Образовательная организация',
                                                  error_messages={"required": "Введите наименование организации"})
    education_organization_address_locality = forms.CharField(max_length=255, label="Населённый пункт",
                                                              error_messages={
                                                                  "required": "Введите населённый пункт"})
    education_organization_address_street = forms.CharField(max_length=255, label='Улица',
                                                            error_messages={
                                                                "required": "Введите улицу"})
    education_organization_address_number_of_building = forms.CharField(max_length=255, label='Номер строения',
                                                                        error_messages={
                                                                            "required": "Введите номер строения"})
    name = forms.CharField(max_length=255, label='Наименование специальности',
                           error_messages={"required": "Введите наименование специальности"})
    code = forms.CharField(max_length=9, label='Код специальности',
                           error_messages={"required": "Введите код специальности"})
    education_level = forms.ModelChoiceField(queryset=EducationLevel.objects.all(),
                                             label='Уровень образования')

    class Meta:
        model = EducationOfJobSeeker
        fields = (
            'education_organization_name', 'education_organization_address_locality',
            'education_organization_address_street', 'education_organization_address_number_of_building', 'name',
            'code', 'education_level',
            'year_received')


class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperience
        fields = ('organization', 'position', 'date_of_employment', 'date_of_dismissal')
        exclude = ['job_seeker', ]

        widgets = {
            'date_of_dismissal': forms.DateInput(attrs={'type': 'date'}),
            'date_of_employment': forms.DateInput(attrs={'type': 'date'}),
        }


class ApplicationResponseRejectForm(forms.ModelForm):
    class Meta:
        model = ApplicationsResponses
        fields = ['description']
