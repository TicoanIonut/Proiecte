# Generated by Django 3.2.5 on 2022-05-16 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magazin', '0002_auto_20220513_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produs',
            name='imagine',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
