# Generated by Django 4.2.7 on 2023-12-04 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0006_skill_softwareandhardwaretool_specialization_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobSeeker',
            fields=[
                ('person_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='domain.person')),
                ('birthdate', models.DateField(verbose_name='Дата рождения')),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='domain.address', verbose_name='Адрес')),
                ('skill', models.ManyToManyField(blank=True, null=True, to='domain.skill', verbose_name='Навыки')),
                ('specialization', models.ManyToManyField(blank=True, null=True, to='domain.specialization', verbose_name='Специализация')),
            ],
            options={
                'verbose_name': 'Соискатель',
                'verbose_name_plural': 'Соискатели',
            },
            bases=('domain.person',),
        ),
        migrations.CreateModel(
            name='WorkExperience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_employment', models.DateField(verbose_name='Дата приёма')),
                ('date_of_dismissal', models.DateField(blank=True, null=True, verbose_name='Дата увольнения')),
                ('organization', models.CharField(max_length=255, verbose_name='Организация')),
                ('position', models.CharField(max_length=255, verbose_name='Должность')),
                ('job_seeker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='domain.jobseeker', verbose_name='Соискатель')),
            ],
            options={
                'verbose_name': 'Опыт работы',
                'verbose_name_plural': 'Опыты работ',
            },
        ),
        migrations.CreateModel(
            name='EducationOfJobSeeker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year_received', models.DateField(verbose_name='Год получениия')),
                ('education', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='domain.education', verbose_name='Образование')),
                ('job_seeker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='domain.jobseeker', verbose_name='Соискатель')),
            ],
            options={
                'verbose_name': 'Образование соискателя',
                'verbose_name_plural': 'Образования соискателей',
            },
        ),
    ]