# Generated by Django 3.2.5 on 2022-05-13 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magazin', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='user',
            new_name='utilizator',
        ),
        migrations.AddField(
            model_name='produs',
            name='imagine',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
