# Generated by Django 4.2.7 on 2023-12-02 09:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0004_employeeposition_employer_employee'),
    ]

    operations = [
        migrations.CreateModel(
            name='EducationLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=90, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Уровень образования',
                'verbose_name_plural': 'Уровни образования',
            },
        ),
        migrations.CreateModel(
            name='EducationalOrganization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование')),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='domain.address', verbose_name='Адрес')),
            ],
            options={
                'verbose_name': 'Образовательное учреждение',
                'verbose_name_plural': 'Образовательные учреждения',
            },
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование')),
                ('code', models.CharField(blank=True, max_length=9, null=True, verbose_name='Код специальности')),
                ('education_level', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='domain.educationlevel', verbose_name='Уровень образования')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='domain.educationalorganization', verbose_name='Образовательное учреждение')),
            ],
            options={
                'verbose_name': 'Образование',
                'verbose_name_plural': 'Образования',
            },
        ),
    ]
