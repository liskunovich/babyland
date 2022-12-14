# Generated by Django 4.1.2 on 2022-11-11 20:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0006_remove_day_total_children'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderrequest',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='clients.client'),
        ),
        migrations.AlterField(
            model_name='orderrequest',
            name='date',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='clients.day'),
        ),
    ]
