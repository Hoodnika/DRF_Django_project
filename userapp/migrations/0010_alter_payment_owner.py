# Generated by Django 5.0.6 on 2024-07-12 19:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0009_rename_user_payment_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payment', to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
    ]
