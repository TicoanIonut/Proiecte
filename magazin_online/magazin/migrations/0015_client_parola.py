# Generated by Django 3.2.5 on 2022-06-02 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magazin', '0014_rename_customer_comanda_client'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='parola',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
