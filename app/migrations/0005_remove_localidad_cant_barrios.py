# Generated by Django 3.1.4 on 2021-10-25 18:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20211025_1843'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='localidad',
            name='cant_barrios',
        ),
    ]
