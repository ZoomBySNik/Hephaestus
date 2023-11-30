from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class CustomUser(AbstractUser):
    patronymic = models.CharField(max_length=255, blank=False, null=False, verbose_name='Отчество')
    phone_number = PhoneNumberField(region="RU", blank=False, null=False, verbose_name='Номер телефона')
    profile_photo = models.ImageField(blank=True, null=True, verbose_name='Фото профиля', upload_to='user_photos')

    def __str__(self):
        return '%s %s %s' % (self.last_name, self.first_name, self.patronymic)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Person(models.Model):
    surname = models.CharField(max_length=255, blank=False, null=False, verbose_name='Фамилия')
    name = models.CharField(max_length=255, blank=False, null=False, verbose_name='Имя')
    patronymic = models.CharField(max_length=255, blank=False, null=False, verbose_name='Отчество')
    email = models.EmailField(blank=False, max_length=254, verbose_name='Почта')
    phone = PhoneNumberField(region="RU", blank=False, null=False, verbose_name='Номер телефона')
    profile_photo = models.ImageField(blank=True, null=True, verbose_name='Фото профиля', upload_to='person_photos')

    def __str__(self):
        return '%s %s %s' % (self.surname, self.name, self.patronymic)

    class Meta:
        verbose_name = 'Индивид'
        verbose_name_plural = 'Индивиды'


class OrganizationalLegalForm(models.Model):
    name = models.CharField(max_length=90, blank=False, null=False, verbose_name='Наименование')
    short_name = models.CharField(max_length=10, blank=False, null=False, verbose_name='Краткое наименование')

    def __str__(self):
        return '%s' % (self.short_name)

    class Meta:
        verbose_name = 'Организационно-правовая форма'
        verbose_name_plural = 'Организационно-правовые формы'
