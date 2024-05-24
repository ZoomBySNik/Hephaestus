import os

from PIL import Image
from django import forms
from django.contrib.auth.forms import UserCreationForm

from domain.models import *


class EmployerRegistrationForm(UserCreationForm):
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'type': 'tel'}), label='Номер телефона')

    class Meta:
        model = Employer
        fields = ['username', 'email', 'last_name', 'first_name', 'patronymic', 'phone_number']


class JobSeekerRegistrationForm(UserCreationForm):
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'type': 'tel'}), label='Номер телефона')

    class Meta:
        model = JobSeeker
        fields = ['username', 'email', 'last_name', 'first_name', 'patronymic', 'phone_number']


class PhotoSaveForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_photo']

    def save(self, commit=True):
        user = super().save(commit=False)
        profile_photo = self.cleaned_data['profile_photo']
        if profile_photo:
            # Сохранение временного изображения для обработки
            user.profile_photo = profile_photo
            if commit:
                user.save()

            # Полный путь к сохраненному изображению
            image_path = user.profile_photo.path

            # Открытие изображения и конвертация в WebP
            img = Image.open(image_path)
            webp_path = os.path.splitext(image_path)[0] + '.webp'
            img.save(webp_path, 'webp')
            # Обновление ссылки на изображение пользователя
            user.profile_photo.name = user.profile_photo.name.rsplit('.', 1)[0] + '.webp'
        if commit:
            user.save()
        return user


class EmployeeForm(forms.ModelForm):
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'type': 'tel'}), label='Номер телефона')
    employee_position = forms.ModelChoiceField(queryset=EmployeePosition.objects.all(), label='Должность')

    class Meta:
        model = Employee
        fields = ['last_name', 'first_name', 'patronymic', 'phone_number', 'email', 'employee_position']


class ApplicationSettingForm(forms.Form):
    start_date = forms.DateField(label='Начальная дата', widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    end_date = forms.DateField(label='Конечная дата', widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    STATUS_CHOICES = Application.STATUS_CHOICES
    status = forms.MultipleChoiceField(choices=STATUS_CHOICES, required=True, widget=forms.CheckboxSelectMultiple,
                                       label='Статусы')
    employer = forms.ModelChoiceField(queryset=Employer.objects.filter(application__isnull=False).distinct(),
                                      required=False, label='Заказчик')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Установите начальное значение для поля status как список всех доступных статусов
        self.fields['status'].initial = [choice[0] for choice in self.STATUS_CHOICES]


class UsersSettingForm(forms.Form):
    USER_TYPES_CHOICES = [
        ('employee', 'Работник'),
        ('employer', 'Работодатель'),
        ('job_seeker', 'Соискатель'),
    ]
    user_types = forms.MultipleChoiceField(choices=USER_TYPES_CHOICES,
                                           required=True,
                                           widget=forms.CheckboxSelectMultiple,
                                           label='Типы пользователей')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Установите начальное значение для поля status как список всех доступных статусов
        self.fields['user_types'].initial = [choice[0] for choice in self.USER_TYPES_CHOICES]
