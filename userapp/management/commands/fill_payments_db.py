from django.core.management import BaseCommand

from courseapp.models import Course, Lesson
from userapp.models import User, Payment


class Command(BaseCommand):

    def handle(self, *args, **options):
        payment_list_create = []
        lesson_list = Lesson.objects.all()
        course_list = Course.objects.all()
        for course in course_list:
            pay = Payment(
                user_id=1,
                cost=30000,
                paid_course_id=course.pk,
                payment_type='transfer'
            )
            payment_list_create.append(pay)
        for lesson in lesson_list:
            pay = Payment(
                user_id=1,
                cost=5000,
                paid_lesson_id=lesson.pk,
                payment_type='cash'
            )
            payment_list_create.append(pay)
        Payment.objects.bulk_create(payment_list_create)
