from django import forms
from domain.models import *
from phonenumber_field.formfields import PhoneNumberField


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
