# Generated by Django 5.0.6 on 2024-07-15 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courseapp', '0006_lesson_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='дата последнего изменения'),
        ),
    ]