# Generated by Django 3.1.4 on 2021-10-25 20:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20211025_1850'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='localidad',
            name='cant_paquetes',
        ),
    ]
