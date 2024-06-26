# Generated by Django 4.2.7 on 2024-04-20 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0011_alter_application_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationsresponses',
            name='status',
            field=models.CharField(choices=[('pending', 'В ожидании'), ('under_review', 'Рассмотрение'), ('sent_to_employer', 'Отправлен к работодателю'), ('accepted', 'Принят'), ('overdue', 'Просрочена'), ('rejected', 'Отклонен'), ('withdrawn', 'Отозван')], default='pending', max_length=20, verbose_name='Статус'),
        ),
    ]
