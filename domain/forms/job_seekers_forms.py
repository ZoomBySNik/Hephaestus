from datetime import timedelta
from datetime import datetime as dt
from django import forms
from django.core.exceptions import ValidationError

from domain.models import *


class JobSeekerForm(forms.ModelForm):
    locality = forms.CharField(max_length=255, label='Населенный пункт', required=False)
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'type': 'tel'}), label='Номер телефона')

    class Meta:
        model = JobSeeker
        fields = ['last_name', 'first_name', 'patronymic', 'phone_number', 'email', 'birthdate', 'locality', 'about',
                  'work_location_preference']
        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
        }


class SkillsForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(queryset=Skill.objects.all().order_by('name'),
                                            widget=forms.CheckboxSelectMultiple,
                                            label='Навыки')
    new_skills = forms.CharField(label='Добавить новые навыки', required=False)

    class Meta:
        model = JobSeeker
        fields = ('skills', 'new_skills')


class SpecializationForm(forms.ModelForm):
    specializations = forms.ModelMultipleChoiceField(queryset=Specialization.objects.all().order_by('name'),
                                                     widget=forms.CheckboxSelectMultiple,
                                                     label='Специализции')
    new_specializations = forms.CharField(label='Добавить новые навыки', required=False)

    class Meta:
        model = JobSeeker
        fields = ('specializations', 'new_specializations')


class SoftwareAndHardwareToolForm(forms.ModelForm):
    software_and_hardware_tools = forms.ModelMultipleChoiceField(
        queryset=SoftwareAndHardwareTool.objects.all().order_by('name'),
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


class JobInterviewForm(forms.ModelForm):
    tomorrow = dt.now() + timedelta(days=1)
    employee = forms.ModelChoiceField(queryset=Employee.objects.all(), label='Сотрудник')
    date_of_interview = forms.DateTimeField(widget=forms.DateTimeInput(attrs={
        'type': 'datetime-local', 'step': 60,
        'min': (dt(tomorrow.year, tomorrow.month, tomorrow.day, 9, 0)),
        'max': (dt.now() + timedelta(
            days=7)).strftime('%Y-%m-%dT%H:%M'),
    }),
        label='Время собеседования')
    locality = forms.CharField(max_length=255, label='Населенный пункт',
                               required=False)
    street = forms.CharField(max_length=255, label='Улица',
                             required=False)
    number_of_building = forms.CharField(max_length=31, label='Номер строения',
                                         required=False)
    apartment_number = forms.CharField(max_length=31, label='Номер помещения',
                                       required=False)

    class Meta:
        model = JobInterview
        fields = ['employee', 'date_of_interview', 'locality', 'street', 'number_of_building', 'apartment_number', 'link']

    def clean(self):
        cleaned_data = super().clean()
        locality = cleaned_data.get('locality')
        street = cleaned_data.get('street')
        number_of_building = cleaned_data.get('number_of_building')
        apartment_number = cleaned_data.get('apartment_number')
        link = cleaned_data.get('link')

        if (locality or street or number_of_building or apartment_number) and link:
            raise ValidationError(
                "Можно заполнить только одно из полей 'Место проведения' или 'Ссылка для онлайн собеседования'")
        elif not (locality or street or number_of_building) and not link:
            raise ValidationError(
                "Необходимо заполнить одно из полей 'Место проведения' или 'Ссылка для онлайн собеседования'")

        return cleaned_data


class ReviewOnInterviewForm(forms.ModelForm):
    interview_description = forms.CharField(label='Отзыв сотрудника', widget=forms.Textarea, required=True)
    CHOICES = [
        ('rejected', 'Отказать'),
        ('sent_to_employer', 'Отправить к работодателю'),
    ]
    response_status = forms.ChoiceField(label='Статус', choices=CHOICES)

    class Meta:
        model = JobInterview
        fields = ['interview_description', 'response_status']
