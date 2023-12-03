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
        return '%s' % self.short_name

    class Meta:
        verbose_name = 'Организационно-правовая форма'
        verbose_name_plural = 'Организационно-правовые формы'


class Address(models.Model):
    locality = models.CharField(max_length=255, blank=False, null=False, verbose_name='Населенный пункт')
    street = models.CharField(max_length=255, blank=True, null=True, verbose_name='Улица')
    number_of_building = models.CharField(max_length=31, blank=True, null=True, verbose_name='Номер строения')
    apartment_number = models.CharField(max_length=31, blank=True, null=True, verbose_name='Номер квартиры/офиса')
    latitude = models.FloatField(blank=True, null=True, verbose_name='Широта')
    longitude = models.FloatField(blank=True, null=True, verbose_name='Долгота')
    map_link = models.URLField(blank=True, null=True, verbose_name='Ссылка на карты')

    def __str__(self):
        return '%s' % self.map_link

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'


class Organization(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False, verbose_name='Наименование')
    payment_account = models.CharField(max_length=20, blank=False, null=False, verbose_name='Расчетный счет')
    organizational_legal_form = models.ForeignKey('OrganizationalLegalForm', on_delete=models.PROTECT,
                                                  null=False, blank=False, verbose_name='ОПФ')
    inn = models.CharField(max_length=12, blank=False, null=False, verbose_name='ИНН')
    address = models.ForeignKey('Address', on_delete=models.PROTECT,
                                null=False, blank=False, verbose_name='Адрес')

    def __str__(self):
        return '%s' % self.name

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'


class Employer(Person):
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE,
                                     null=False, blank=False, verbose_name='Организация')
    position = models.CharField(max_length=90, blank=False, null=False, verbose_name='Должность')

    def __str__(self):
        return '%s %s %s' % (self.surname, self.name, self.organization.name)

    class Meta:
        verbose_name = 'Работодатель'
        verbose_name_plural = 'Работодатели'


class EmployeePosition(models.Model):
    name = models.CharField(max_length=90, blank=False, null=False, verbose_name='Наименование')

    def __str__(self):
        return '%s' % self.name

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'


class Employee(CustomUser):
    date_of_employment = models.DateField(blank=False, null=False, verbose_name='Дата приёма')
    date_of_dismissal = models.DateField(blank=True, null=True, verbose_name='Дата увольнения')
    employee_position = models.ForeignKey('EmployeePosition', on_delete=models.PROTECT,
                                          null=False, blank=False, verbose_name='Должность')

    def __str__(self):
        return '%s %s %s' % (self.last_name, self.first_name, self.employee_position.name)

    class Meta:
        verbose_name = 'Работник'
        verbose_name_plural = 'Работники'


class EducationalOrganization(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False, verbose_name='Наименование')
    address = models.ForeignKey('Address', on_delete=models.PROTECT,
                                null=False, blank=False, verbose_name='Адрес')

    def __str__(self):
        return '%s' % self.name

    class Meta:
        verbose_name = 'Образовательное учреждение'
        verbose_name_plural = 'Образовательные учреждения'


class EducationLevel(models.Model):
    name = models.CharField(max_length=90, blank=False, null=False, verbose_name='Наименование')

    def __str__(self):
        return '%s' % self.name

    class Meta:
        verbose_name = 'Уровень образования'
        verbose_name_plural = 'Уровни образования'


class Education(models.Model):
    organization = models.ForeignKey('EducationalOrganization', on_delete=models.PROTECT,
                                     null=False, blank=False, verbose_name='Образовательное учреждение')
    name = models.CharField(max_length=255, blank=False, null=False, verbose_name='Наименование')
    code = models.CharField(max_length=9, blank=True, null=True, verbose_name='Код специальности')
    education_level = models.ForeignKey('EducationLevel', on_delete=models.PROTECT, null=False, blank=False,
                                        verbose_name='Уровень образования')

    def __str__(self):
        return '%s %s %s' % (self.name, self.code, self.organization)

    class Meta:
        verbose_name = 'Образование'
        verbose_name_plural = 'Образования'


class Skill(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, verbose_name='Наименование')

    def __str__(self):
        return '%s' % self.name

    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'


class Specialization(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False, verbose_name='Наименование')

    def __str__(self):
        return '%s' % self.name

    class Meta:
        verbose_name = 'Специализация'
        verbose_name_plural = 'Специализации'


class SoftwareAndHardwareTool(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False, verbose_name='Наименование')

    def __str__(self):
        return '%s' % self.name

    class Meta:
        verbose_name = 'Программно-техническое средство'
        verbose_name_plural = 'Программно-технические средства'


class WorkSchedule(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False, verbose_name='Наименование')

    def __str__(self):
        return '%s' % self.name

    class Meta:
        verbose_name = 'График работы'
        verbose_name_plural = 'Графики работы'
