from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

from config.settings import AUTH_USER_MODEL
from config.special_elements import NULLABLE


class Course(models.Model):
    title = models.CharField(max_length=300, verbose_name='название')
    preview = models.ImageField(**NULLABLE, upload_to='courses/preview', verbose_name='превью (картинка)')
    description = models.TextField(verbose_name='описание')
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='владелец', **NULLABLE)
    updated_at = models.DateTimeField(verbose_name='дата последнего изменения', auto_now=True, **NULLABLE)

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
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='владелец', **NULLABLE)
    price = models.PositiveIntegerField(verbose_name='Стоимость урока', default=1000)
    updated_at = models.DateTimeField(verbose_name='дата последнего изменения', auto_now=True, **NULLABLE)

    def __str__(self):
        return f'{self.title} ({self.course})'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Subscription(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь',
                             related_name='subscription')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс', related_name='subscription')


@receiver(pre_save, sender=Lesson)
def update_course_updated_at(sender, instance, **kwargs):
    if instance.course:
        instance.course.updated_at = timezone.now()
        instance.course.save()
