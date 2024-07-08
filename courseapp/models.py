from django.db import models

from config.special_elements import NULLABLE


class Course(models.Model):
    title = models.CharField(max_length=300, verbose_name='название')
    preview = models.ImageField(**NULLABLE, upload_to='courses/preview', verbose_name='превью (картинка)')
    description = models.TextField(verbose_name='описание')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=300, verbose_name='название')
    preview = models.ImageField(**NULLABLE, upload_to='lessons/preview', verbose_name='превью (картинка)')
    description = models.TextField(verbose_name='описание')
    url = models.TextField(verbose_name='ссылка на видео')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс', related_name='lesson')

    def __str__(self):
        return f'{self.title} ({self.course})'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
