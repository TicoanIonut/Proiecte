# Generated by Django 3.2.5 on 2022-06-01 08:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('magazin', '0013_rename_client_comanda_customer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comanda',
            old_name='customer',
            new_name='client',
        ),
    ]
