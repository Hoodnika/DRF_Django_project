import time

from django.core.mail import send_mail
from django.utils import timezone
from celery import shared_task
from django.shortcuts import get_object_or_404

from config.settings import EMAIL_HOST_USER
from courseapp.models import Course, Subscription
from userapp.models import User


def check_last_update_time():
    pass


@shared_task()
def send_course_update_info(course_id):
    # time.sleep(61)
    time.sleep(14401)
    course = get_object_or_404(Course, pk=course_id)
    last_update_at = course.updated_at

    # print('start checking')
    # if timezone.now() - last_update_at > timezone.timedelta(minutes=1):
    if timezone.now() - last_update_at > timezone.timedelta(hours=4):
        subscriptions = Subscription.objects.filter(course=course)
        # print('yes-yes-yes')
        for subscription in subscriptions:
            send_mail(
                subject='Ваш курс обновлен!',
                message=f"Материал из курса {course.title}, на который вы подписались был обновлен",
                from_email=EMAIL_HOST_USER,
                recipient_list=[subscription.user.email],
                fail_silently=True,
            )


@shared_task()
def check_last_login():
    users = User.objects.filter(is_active=True)
    for user in users:
        if user.last_login is None:
            user.is_active = False
            user.save()
        elif timezone.now() - user.last_login > timezone.timedelta(days=30):
            user.is_active = False
            user.save()
            # send_mail(
            #     subject="Упс, грустные новости((",
            #     message=f"Вы были заблокированы в DRF_Django_project, так как не заходили в систему за последние 30 дней",
            #     from_email=EMAIL_HOST_USER,
            #     recipient_list=[user.email],
            #     fail_silently=True,
            # )
