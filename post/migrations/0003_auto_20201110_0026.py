# Generated by Django 3.1.1 on 2020-11-09 18:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_auto_20201102_0834'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='msg',
            new_name='caption',
        ),
        migrations.RemoveField(
            model_name='post',
            name='subject',
        ),
    ]
