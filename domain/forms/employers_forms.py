from datetime import timedelta
from datetime import datetime as dt
from django import forms
from domain.models import *


class EmployerForm(forms.ModelForm):
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'type': 'tel'}), label='Номер телефона')
    position = forms.CharField(max_length=90, required=False, label='Должность')

    class Meta:
        model = Employer
        fields = ['last_name', 'first_name', 'patronymic', 'phone_number', 'email', 'position']


class OrganizationForm(forms.ModelForm):
    locality = forms.CharField(max_length=255, label='Населенный пункт',
                               error_messages={"required": "Введите населённый пункт"})
    street = forms.CharField(max_length=255, label='Улица',
                             error_messages={"required": "Введите улицу"})
    number_of_building = forms.CharField(max_length=31, label='Номер строения',
                                         error_messages={"required": "Введите номер строения"})
    apartment_number = forms.CharField(max_length=31, label='Номер помещения',
                                       required=False)

    class Meta:
        model = Organization
        exclude = ['address']
        fields = '__all__'

    field_group_address = [locality, street, number_of_building, apartment_number]


class ApplicationForm(forms.ModelForm):
    min_desired_date = (dt.now() + timedelta(days=10)).strftime('%Y-%m-%d')
    min_final_date = (dt.now() + timedelta(days=14)).strftime('%Y-%m-%d')
    position = forms.ModelChoiceField(queryset=Position.objects.all(), label='Должность')
    specialization = forms.ModelChoiceField(queryset=Specialization.objects.all(), label='Специализация')
    education_level = forms.ModelChoiceField(queryset=EducationLevel.objects.all(), required=False,
                                             label='Уровень образования')
    salary = forms.CharField(max_length=255, label='Зарплата (руб.)')
    desired_date = forms.DateField(label='Желательный срок исполнения',
                                   widget=forms.DateInput(attrs={'type': 'date', 'min': min_desired_date}), )
    final_date = forms.DateField(label='Последний срок исполнения',
                                 widget=forms.DateInput(attrs={'type': 'date', 'min': min_final_date}), )
    skills = forms.ModelMultipleChoiceField(queryset=Skill.objects.all(), widget=forms.CheckboxSelectMultiple,
                                            required=False, label='Навыки')
    software_and_hardware_tools = forms.ModelMultipleChoiceField(queryset=SoftwareAndHardwareTool.objects.all(),
                                                                 required=False,
                                                                 widget=forms.CheckboxSelectMultiple,
                                                                 label='Требуемые программно-технические средства')
    experience = forms.IntegerField(label='Опыт(лет)')
    work_schedule = forms.ModelChoiceField(queryset=WorkSchedule.objects.all(), label='График работы')

    class Meta:
        model = Application
        fields = ['position', 'salary', 'desired_date', 'final_date', 'specialization', 'education_level', 'skills',
                  'software_and_hardware_tools',
                  'experience', 'work_schedule']


class ChangeStateOfApplicationForm(forms.ModelForm):
    status = forms.ChoiceField(choices=[
        ('new', 'Новая'),
        ('in_progress', 'В обработке'),
        ('pending_approval', 'На согласовании'),
        ('canceled', 'Отменена'),
    ], label='Статус')

    class Meta:
        model = Application
        fields = ['status']
