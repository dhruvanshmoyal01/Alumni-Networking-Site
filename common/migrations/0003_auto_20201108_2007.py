# Generated by Django 3.1.1 on 2020-11-08 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date_of_event',
            field=models.DateField(),
        ),
    ]
