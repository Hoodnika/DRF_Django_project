# Generated by Django 5.0.6 on 2024-07-08 20:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0003_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='datetime_payment',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='дата оплаты'),
        ),
    ]
