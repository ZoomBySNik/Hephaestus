# Generated by Django 4.2.7 on 2024-05-07 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0019_alter_educationofjobseeker_document_confirmation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='educationofjobseeker',
            name='year_received',
            field=models.IntegerField(choices=[], verbose_name='Год получения'),
        ),
    ]
