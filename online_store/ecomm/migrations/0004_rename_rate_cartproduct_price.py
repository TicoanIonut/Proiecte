# Generated by Django 4.0.4 on 2022-12-10 21:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecomm', '0003_rename_price_cartproduct_rate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartproduct',
            old_name='rate',
            new_name='price',
        ),
    ]
