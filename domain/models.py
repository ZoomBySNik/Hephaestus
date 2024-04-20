import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class CustomUser(AbstractUser):
    patronymic = models.CharField(max_length=255, blank=False, null=False, verbose_name='Отчество')
    phone_number = models.CharField(max_length=18, blank=False, null=False, verbose_name='Номер телефона')
    profile_photo = models.ImageField(blank=True, null=True, verbose_name='Фото профиля', upload_to='user_photos')

    def __str__(self):
        return '%s %s %s' % (self.last_name, self.first_name, self.patronymic)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


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
    map_link = models.URLField(max_length=2083, blank=True, null=True, verbose_name='Ссылка на карты')

    def __str__(self):
        return '%s' % self.map_link

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'


class Organization(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False, verbose_name='Наименование')
    payment_account = models.CharField(max_length=20, blank=False, null=False, verbose_name='Расчетный счет')
    okved_kode = models.CharField(max_length=9, blank=True, null=True, verbose_name='Код ОКВЭД')
    organizational_legal_form = models.ForeignKey('OrganizationalLegalForm', on_delete=models.PROTECT,
                                                  null=False, blank=False, verbose_name='ОПФ')
    inn = models.CharField(max_length=12, blank=False, null=False, verbose_name='ИНН')
    address = models.ForeignKey('Address', on_delete=models.PROTECT,
                                null=False, blank=False, verbose_name='Адрес')
    about = models.TextField(blank=True, null=True, verbose_name='Описание профиля')
    organization_logo = models.ImageField(blank=True, null=True, verbose_name='Логотип организации', upload_to='organization_logos')

    def __str__(self):
        return '%s' % self.name

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'


class Employer(CustomUser):
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE,
                                     blank=True, null=True, verbose_name='Организация')
    position = models.CharField(max_length=90, blank=True, null=True, verbose_name='Должность')

    def __str__(self):
        return '%s %s' % (self.last_name, self.first_name)

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
    date_of_employment = models.DateField(blank=True, null=True, verbose_name='Дата приёма', auto_now=True)
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
    code = models.IntegerField(validators=[
            MinValueValidator(0), MaxValueValidator(10)], blank=False, null=False,
                               verbose_name='Код уровня профессионального образования')

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


class JobSeeker(CustomUser):
    birthdate = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    address = models.ForeignKey('Address', blank=True, null=True, on_delete=models.PROTECT, verbose_name='Адрес')
    skill = models.ManyToManyField('Skill', blank=True, verbose_name='Навыки')
    specialization = models.ManyToManyField('Specialization', blank=True, verbose_name='Специализация')
    about = models.TextField(blank=True, null=True, verbose_name='Описание организации')

    def __str__(self):
        return '%s %s %s' % (self.last_name, self.first_name, self.birthdate.isoformat())

    class Meta:
        verbose_name = 'Соискатель'
        verbose_name_plural = 'Соискатели'


class WorkExperience(models.Model):
    job_seeker = models.ForeignKey('JobSeeker', blank=False, null=False,
                                   on_delete=models.CASCADE, verbose_name='Соискатель')
    date_of_employment = models.DateField(blank=False, null=False, verbose_name='Дата приёма')
    date_of_dismissal = models.DateField(blank=True, null=True, verbose_name='Дата увольнения')
    organization = models.CharField(max_length=255, blank=False, null=False, verbose_name='Организация')
    position = models.ForeignKey('Position', blank=False, null=False,
                                 on_delete=models.PROTECT, verbose_name='Должность')

    def __str__(self):
        return '%s %s лет %s' % \
            (self.job_seeker.__str__(),
             ((self.date_of_dismissal - self.date_of_employment
               if self.date_of_dismissal else datetime.date.today() - self.date_of_employment).days) // 365,
             self.position)

    class Meta:
        verbose_name = 'Опыт работы'
        verbose_name_plural = 'Опыты работ'


class Position(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False, verbose_name='Наименование')

    def __str__(self):
        return '%s' % self.name

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должность'


class EducationOfJobSeeker(models.Model):
    job_seeker = models.ForeignKey('JobSeeker', blank=False, null=False,
                                   on_delete=models.CASCADE, verbose_name='Соискатель')
    education = models.ForeignKey('Education', blank=False, null=False,
                                  on_delete=models.PROTECT, verbose_name='Образование')
    year_choices = [(year, str(year)) for year in range(1980, datetime.datetime.now().year + 1)]
    year_received = models.IntegerField(choices=year_choices, blank=False, null=False, verbose_name='Год получения')

    def __str__(self):
        return '%s %s лет %s' % (self.job_seeker.__str__(), self.education.__str__(), self.year_received)

    class Meta:
        verbose_name = 'Образование соискателя'
        verbose_name_plural = 'Образования соискателей'


class SoftwareAndHardwareToolOfJobSeeker(models.Model):
    job_seeker = models.ForeignKey('JobSeeker', blank=False, null=False,
                                   on_delete=models.CASCADE, verbose_name='Соискатель')
    software_and_hardware_tool = models.ForeignKey('SoftwareAndHardwareTool', blank=False, null=False,
                                                   on_delete=models.CASCADE,
                                                   verbose_name='Программно-техническое средство')
    proficiency_level = models.CharField(max_length=20, blank=True, null=True, verbose_name='Уровень владения')
    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий')

    def __str__(self):
        return '%s %s' % (self.job_seeker.__str__(), self.software_and_hardware_tool.name)

    class Meta:
        verbose_name = 'Уровень владения программно-техническим средством'
        verbose_name_plural = 'Уровни владения программно-техническими средствами'


class Publication(models.Model):
    job_seeker = models.ForeignKey('JobSeeker', blank=False, null=False,
                                   on_delete=models.CASCADE, verbose_name='Соискатель')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    time_of_publication = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Время публикации')
    time_of_moderation = models.DateTimeField(null=True, blank=True, verbose_name='Время модерации')
    time_of_edition = models.DateTimeField(null=True, blank=True, verbose_name='Время изменения')
    software_and_hardware_tool = models.ManyToManyField('SoftwareAndHardwareTool', blank=True,
                                                        verbose_name='Программно-техническое средство')

    def __str__(self):
        return 'Публикация %s от %s' % (self.job_seeker.__str__(), self.time_of_publication)

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'


class AttachmentToPublication(models.Model):
    publication = models.ForeignKey('Publication', blank=False, null=False, on_delete=models.CASCADE)
    file = models.FileField(blank=False, null=False,
                            verbose_name='Приложение к публикации', upload_to='attachment_to_publications')

    def __str__(self):
        return 'Приложение к (%s): %s' % (self.publication.__str__(), self.file.name)

    class Meta:
        verbose_name = 'Приложение к публикации'
        verbose_name_plural = 'Приложения к публикациям'


class Application(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'В обработке'),
        ('pending_approval', 'На согласовании'),
        ('completed', 'Завершена'),
        ('overdue', 'Просрочена'),
        ('canceled', 'Отменена'),
    ]
    employer = models.ForeignKey('Employer', blank=False, null=False,
                                 on_delete=models.CASCADE, verbose_name='Работодатель')
    date_of_application = models.DateTimeField(blank=False, null=False, auto_now_add=True,
                                               editable=False, verbose_name='Дата заявки')
    desired_date = models.DateField(blank=True, null=True, verbose_name='Желательный срок')
    final_date = models.DateField(blank=True, null=True, verbose_name='Крайний срок')
    position = models.ForeignKey('Position', blank=False, null=False,
                                 on_delete=models.PROTECT, verbose_name='Должность')
    salary = models.CharField(blank=False, null=False, max_length=255, verbose_name='Зарплата')
    specialization = models.ForeignKey('Specialization', blank=False, null=False,
                                       on_delete=models.PROTECT, verbose_name='Специализация')
    education_level = models.ForeignKey('EducationLevel', blank=True, null=True,
                                        on_delete=models.PROTECT, verbose_name='Уровень образования')
    skills = models.ManyToManyField('Skill', blank=True, verbose_name='Навыки')
    software_and_hardware_tools = models.ManyToManyField('SoftwareAndHardwareTool', blank=True,
                                                         verbose_name='Требуемые программно-технические средства')
    experience = models.IntegerField(blank=False, null=False, default=0, verbose_name='Опыт (лет)')
    work_schedule = models.ForeignKey('WorkSchedule', blank=False, null=False,
                                      on_delete=models.PROTECT, verbose_name='График работы')
    employee = models.ForeignKey('Employee', blank=True, null=True,
                                 on_delete=models.PROTECT, verbose_name='Работник')
    date_of_completion = models.DateField(blank=True, null=True, verbose_name='Дата выполнения')
    date_of_cancellation = models.DateField(blank=True, null=True, verbose_name='Дата отмены')
    status = models.CharField(blank=False, null=False, max_length=20, choices=STATUS_CHOICES,
                              default='new', verbose_name='Статус')

    def __str__(self):
        return 'Заявка %s от %s на должность %s' % (self.employer.__str__, self.skills.__str__, self.position)

    class Meta:
        verbose_name = 'Заявка на подбор специалиста'
        verbose_name_plural = 'Заявки на подбор специалистов'


class ApplicationsResponses(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('under_review', 'Рассмотрение'),
        ('sent_to_employer', 'Отправлен к работодателю'),
        ('accepted', 'Принят'),
        ('overdue', 'Просрочена'),
        ('rejected', 'Отклонен'),
        ('withdrawn', 'Отозван'),
    ]
    application = models.ForeignKey('Application', blank=False, null=False,
                                    on_delete=models.CASCADE, verbose_name='Заявка на подбор')
    job_seeker = models.ForeignKey('JobSeeker', blank=False, null=False,
                                   on_delete=models.CASCADE, verbose_name='Соискатель')
    date_of_response = models.DateTimeField(blank=False, null=False, auto_now_add=True,
                                            editable=False, verbose_name='Дата отклика на заявку')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    evaluation = models.FloatField(blank=False, null=False, verbose_name='Предварительная оценка соответствия '
                                                                         'соискателя')

    def __str__(self):
        return 'Отклик на заявку "%s" от %s' % (self.application.__str__, self.job_seeker.__str__)

    class Meta:
        verbose_name = 'Отклик на заявку'
        verbose_name_plural = 'Отклики на заявки'


class JobInterview(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('accepted', 'Принят'),
        ('rejected', 'Отклонен'),
        ('overdue', 'Просрочена'),
        ('passed', 'Прошло'),
        ('with_feedback', 'С отзывом'),
    ]

    application_response = models.ForeignKey('ApplicationsResponses', blank=False, null=False,
                                    on_delete=models.CASCADE, verbose_name='Отклик на заявку')
    employee = models.ForeignKey('Employee', blank=False, null=False,
                                   on_delete=models.CASCADE, verbose_name='Сотрудник')
    date_of_interview = models.DateTimeField(blank=False, null=False, verbose_name='Время собеседования')
    description = models.TextField(blank=True, null=True, verbose_name='Отзыв сотрудника')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')

    def __str__(self):
        return 'Собеседование с "%s" от %s' % (self.application_response.job_seeker.__str__, self.date_of_interview.date)

    class Meta:
        verbose_name = 'Собеседование'
        verbose_name_plural = 'Собеседования'
