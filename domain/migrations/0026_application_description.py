# Generated by Django 4.2.7 on 2024-05-25 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0025_alter_softwareandhardwaretool_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание вакансии'),
        ),
    ]