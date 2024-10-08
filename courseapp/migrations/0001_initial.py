# Generated by Django 5.0.6 on 2024-07-07 21:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='название')),
                ('preview', models.ImageField(blank=True, null=True, upload_to='courses/preview', verbose_name='превью (картинка)')),
                ('description', models.TextField(verbose_name='описание')),
            ],
            options={
                'verbose_name': 'курс',
                'verbose_name_plural': 'курсы',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='название')),
                ('preview', models.ImageField(blank=True, null=True, upload_to='lessons/preview', verbose_name='превью (картинка)')),
                ('description', models.TextField(verbose_name='описание')),
                ('url', models.TextField(verbose_name='ссылка на видео')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courseapp.course', verbose_name='курс')),
            ],
            options={
                'verbose_name': 'урок',
                'verbose_name_plural': 'уроки',
            },
        ),
    ]
