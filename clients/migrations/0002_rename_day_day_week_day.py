# Generated by Django 4.1.2 on 2022-10-23 23:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='day',
            old_name='day',
            new_name='week_day',
        ),
    ]