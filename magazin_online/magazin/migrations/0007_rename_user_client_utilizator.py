# Generated by Django 3.2.5 on 2022-05-30 11:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('magazin', '0006_auto_20220530_1405'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='user',
            new_name='utilizator',
        ),
    ]
