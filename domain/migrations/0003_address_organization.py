# Generated by Django 4.2.7 on 2023-12-01 11:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0002_organizationallegalform_person_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('locality', models.CharField(max_length=255, verbose_name='Населенный пункт')),
                ('street', models.CharField(blank=True, max_length=255, null=True, verbose_name='Улица')),
                ('number_of_building', models.CharField(blank=True, max_length=31, null=True, verbose_name='Номер строения')),
                ('apartment_number', models.CharField(blank=True, max_length=31, null=True, verbose_name='Номер квартиры/офиса')),
                ('latitude', models.FloatField(blank=True, null=True, verbose_name='Широта')),
                ('longitude', models.FloatField(blank=True, null=True, verbose_name='Долгота')),
                ('map_link', models.URLField(blank=True, null=True, verbose_name='Ссылка на карты')),
            ],
            options={
                'verbose_name': 'Адрес',
                'verbose_name_plural': 'Адреса',
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование')),
                ('payment_account', models.CharField(max_length=20, verbose_name='Расчетный счет')),
                ('inn', models.CharField(max_length=12, verbose_name='ИНН')),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='domain.address', verbose_name='Адрес')),
                ('organizational_legal_form', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='domain.organizationallegalform', verbose_name='ОПФ')),
            ],
            options={
                'verbose_name': 'Организация',
                'verbose_name_plural': 'Организации',
            },
        ),
    ]
