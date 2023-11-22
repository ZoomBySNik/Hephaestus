from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
class User(AbstractUser):
    patronymic = models.CharField(max_length=255, blank=False, null=False, verbose_name='Отчество')
    phone_number = PhoneNumberField(region="RU", blank=False, null=False, verbose_name='Номер телефона')
    profile_photo = models.ImageField(blank=True, null=True, verbose_name='Фото профиля', upload_to='user_photos')

    def __str__(self):
        return '%s %s %s' % (self.first_name, self.patronymic, self.last_name)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'