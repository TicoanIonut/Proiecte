# Generated by Django 3.2.5 on 2022-06-29 18:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketApp', '0004_usercreate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='active',
        ),
    ]
