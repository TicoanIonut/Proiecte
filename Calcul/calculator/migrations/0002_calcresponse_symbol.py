# Generated by Django 4.0.4 on 2023-02-09 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='calcresponse',
            name='symbol',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
