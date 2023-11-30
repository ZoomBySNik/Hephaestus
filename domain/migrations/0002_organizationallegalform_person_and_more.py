# Generated by Django 4.2.7 on 2023-11-30 20:19

import django.contrib.auth.validators
from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationalLegalForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=90, verbose_name='Наименование')),
                ('short_name', models.CharField(max_length=10, verbose_name='Краткое наименование')),
            ],
            options={
                'verbose_name': 'Организационно-правовая форма',
                'verbose_name_plural': 'Организационно-правовые формы',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=255, verbose_name='Фамилия')),
                ('name', models.CharField(max_length=255, verbose_name='Имя')),
                ('patronymic', models.CharField(max_length=255, verbose_name='Отчество')),
                ('email', models.EmailField(max_length=254, verbose_name='Почта')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region='RU', verbose_name='Номер телефона')),
                ('profile_photo', models.ImageField(blank=True, null=True, upload_to='person_photos', verbose_name='Фото профиля')),
            ],
            options={
                'verbose_name': 'Индивид',
                'verbose_name_plural': 'Индивиды',
            },
        ),
        migrations.AlterModelOptions(
            name='custominadminuser',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='last name'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username'),
        ),
    ]
