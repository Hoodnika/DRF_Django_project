import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from courseapp.models import Course, Lesson, Subscription
from userapp.models import User


class CourseTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@test.com')
        self.client.force_authenticate(user=self.user)
        self.course_stranger = Course.objects.create(title='title_course_test',
                                                     description='desc_course_test')  # FIRST CREATING !It's IMPORTANT!
        self.course_personal = Course.objects.create(
            title='title_course_personal_test',
            description='desc_course_personal_test',
            owner=self.user
        )  # SECOND CREATING !It's IMPORTANT!

    def test_create_course(self):
        url = reverse('courseapp:courses-list')
        data = {
            'title': 'title_course_personal_test',
            'lesson': [],
            'description': 'desc_course_personal_test',
        }

        response = self.client.post(url, data=data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data.get('title'), self.course_personal.title)
        self.assertEqual(data.get('description'), self.course_personal.description)

    def test_update_personal_course(self):
        url = reverse('courseapp:courses-detail', args=(self.course_personal.pk,))
        data = {
            'title': 'new_title_course_test',
            'description': 'new_desc_course_test',
        }
        response = self.client.patch(url, data=data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('title'), 'new_title_course_test')
        self.assertEqual(data.get('description'), 'new_desc_course_test')

    def test_update_stranger_course(self):
        url = reverse('courseapp:courses-detail', args=(self.course_stranger.pk,))
        data = {
            'title': 'new_title_course_test',
            'description': 'new_desc_course_test',
        }
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_courses(self):
        url = reverse('courseapp:courses-list')
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_result = [
            {
                'id': self.course_stranger.pk,
                'lessons_count': 0,
                'lesson': [],
                'title': self.course_stranger.title,
                'preview': None,
                'description': self.course_stranger.description,
                'owner': None
            },
            {
                'id': self.course_personal.pk,
                'lessons_count': 0,
                'lesson': [],
                'title': self.course_personal.title,
                'preview': None,
                'description': self.course_personal.description,
                'owner': self.course_personal.owner_id
            }
        ]

        self.assertEqual(data.get('results'), expected_result)

    def test_retrieve_personal_course(self):
        url = reverse('courseapp:courses-detail', args=(self.course_personal.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('title'), self.course_personal.title)
        self.assertEqual(data.get('description'), self.course_personal.description)

    def test_retrieve_stranger_course(self):
        url = reverse('courseapp:courses-detail', args=(self.course_stranger.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_personal_course(self):
        url = reverse('courseapp:courses-detail', args=(self.course_personal.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_stranger_course(self):
        url = reverse('courseapp:courses-detail', args=(self.course_stranger.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@test.com')
        self.user_stranger = User.objects.create(email='test_2@test.com')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title='title_course_test', description='desc_course_test')
        self.lesson_personal = Lesson.objects.create(
            title='title_lesson_personal_test',
            description='desc_lesson_personal_test',
            url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',  # <---- little Easter Egg, check it out
            course=self.course,
            owner=self.user
        )
        self.lesson_stranger = Lesson.objects.create(
            title='title_lesson_test',
            description='desc_lesson_test',
            url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            course=self.course,
            owner=self.user_stranger
        )

    def test_create_lesson(self):
        url = reverse('courseapp:lesson_create')
        data = {
            'title': 'title_lesson_personal_test',
            'description': 'desc_lesson_personal_test',
            'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'course': self.course.pk,
            'owner': self.user.pk
        }
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(data.get('title'), self.lesson_personal.title)
        self.assertEqual(data.get('description'), self.lesson_personal.description)
        self.assertEqual(data.get('url'), self.lesson_personal.url)
        self.assertEqual(data.get('course'), self.lesson_personal.course_id)
        self.assertEqual(data.get('owner'), self.lesson_personal.owner_id)

    def test_list_lessons(self):
        url = reverse('courseapp:lesson_list')
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_result = [
            {
                'id': self.lesson_personal.pk,
                'title': self.lesson_personal.title,
                'preview': None,
                'description': self.lesson_personal.description,
                'url': self.lesson_personal.url,
                'course': self.lesson_personal.course_id,
                'owner': self.lesson_personal.owner_id
            },
            {
                'id': self.lesson_stranger.pk,
                'title': self.lesson_stranger.title,
                'preview': None,
                'description': self.lesson_stranger.description,
                'url': self.lesson_stranger.url,
                'course': self.lesson_stranger.course_id,
                'owner': self.lesson_stranger.owner_id
            }
        ]
        self.assertEqual(data.get('results'), expected_result)

    def test_update_personal_lesson(self):
        url = reverse('courseapp:lesson_update', args=(self.lesson_personal.pk,))
        data = {
            'title': self.lesson_personal.title,
            'description': 'new_desc_lesson_test',
            'url': 'https://www.youtube.com/watch?v=XD5w6r-tqXE',
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('title'), self.lesson_personal.title)
        self.assertEqual(data.get('description'), 'new_desc_lesson_test')
        self.assertEqual(data.get('url'), 'https://www.youtube.com/watch?v=XD5w6r-tqXE')

    def test_update_stranger_lesson(self):
        url = reverse('courseapp:lesson_update', args=(self.lesson_stranger.pk,))
        data = {
            'title': self.lesson_stranger.title,
            'description': 'new_desc_lesson_test',
            'url': 'https://www.youtube.com/watch?v=XD5w6r-tqXE',
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_lesson(self):
        url = reverse('courseapp:lesson_get', args=(self.lesson_personal.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('title'), self.lesson_personal.title)
        self.assertEqual(data.get('description'), self.lesson_personal.description)
        self.assertEqual(data.get('url'), self.lesson_personal.url)

    def test_delete_stranger_lesson(self):
        url = reverse('courseapp:lesson_delete', args=(self.lesson_stranger.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_personal_lesson(self):
        url = reverse('courseapp:lesson_delete', args=(self.lesson_personal.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@test.com')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title='title_course_test', description='desc_course_test')
        self.course_2 = Course.objects.create(title='title_2_course_test', description='desc_2_course_test')
        self.subscription = Subscription.objects.create(user=self.user, course=self.course_2)
        self.url = reverse('courseapp:subscription_create')

    def test_activate_sub(self):
        data = {
            'user': self.user.pk,
            'course': self.course.pk
        }
        response = self.client.post(self.url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('message'), 'Подписка на курс title_course_test успешно оформлена')

    def test_deactivate_sub(self):
        data = {
            'user': self.user.pk,
            'course': self.course_2.pk
        }
        response = self.client.post(self.url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('message'), 'Подписка на курс title_2_course_test отменена')
