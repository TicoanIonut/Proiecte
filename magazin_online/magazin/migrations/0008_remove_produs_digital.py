# Generated by Django 3.2.5 on 2022-05-31 11:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('magazin', '0007_rename_user_client_utilizator'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produs',
            name='digital',
        ),
    ]
