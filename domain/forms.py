from django import forms
from domain.models import *


class EmployerForm(forms.ModelForm):
    surname = forms.CharField(max_length=90, label='Фамилия', error_messages={"required": "Введите фамилию"})
    name = forms.CharField(max_length=90, label='Имя', error_messages={"required": "Введите имя"})
    patronymic = forms.CharField(max_length=90, label='Отчество', error_messages={"required": "Введите отчество"})
    email = forms.EmailField(label='Почта', error_messages={"required": "Введите почту"})
    phone = forms.CharField(max_length=18, label='Номер телефона', error_messages={"required": "Введите номер телефона"})
    profile_photo = forms.ImageField(label='Фото профиля', required=False)

    class Meta:
        model = Employer
        fields = ('surname', 'name', 'patronymic', 'phone', 'email', 'profile_photo')


class OrganizationForm(forms.ModelForm):
    position = forms.CharField(max_length=90, label='Должность',
                               error_messages={"required": "Введите должность"})
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
