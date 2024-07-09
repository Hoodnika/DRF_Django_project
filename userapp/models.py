from django.contrib.auth.models import AbstractUser
from django.db import models

from config.settings import AUTH_USER_MODEL
from config.special_elements import NULLABLE
from courseapp.models import Course, Lesson


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='электронная почта', help_text='обязательное поле')
    phone = models.CharField(max_length=50, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    country = models.CharField(max_length=50, verbose_name='страна', **NULLABLE)
    # token_verification = models.CharField(max_length=50, verbose_name='код верификации', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Payment(models.Model):
    class Type_payment(models.TextChoices):
        cash = 'Наличные'
        transfer = 'Переводом'

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь', related_name='payment', **NULLABLE)
    datetime_payment = models.DateTimeField(verbose_name='дата оплаты', auto_now_add=True)
    cost = models.PositiveIntegerField(verbose_name='сумма оплаты')

    # class Paid_material(models.Choices):
    #     Course = Course
    #     Lesson = Lesson
    #
    # paid_material = models.ForeignKey(choices=Paid_material.choices, on_delete=models.CASCADE, verbose_name='оплаченный материал')

    paid_course = models.ForeignKey(Course, on_delete=models.SET_NULL, **NULLABLE, related_name='payment')
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, **NULLABLE, related_name='payment')
    payment_type = models.CharField(choices=Type_payment.choices, max_length=16, verbose_name='способ оплаты')

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'
