from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from courseapp.models import Course, Lesson, Subscription
from courseapp.paginators import CustomPagination
from courseapp.serializer import CourseSerializer, LessonSerializer, CourseDetailSerializer, SubscriptionSerializer
from userapp.permissions import IsModer, IsOwner


########COURSE#########
class CourseViewSet(viewsets.ModelViewSet):
    """
    'API endpoint' для Курсов, имеет вложенный список 'results' в котором хранятся
    данные о Уроках, которые принадлежат соответствующему Курсу
    """
    queryset = Course.objects.all()
    pagination_class = CustomPagination

    def get_serializer_class(self):
        """
        В зависимости от метода обращения выбирается определенный сериализатор
        Детальнее о сериазатораха читайте dogstrings у самих сериализаторов
        """
        if self.action in ['create', 'update']:
            return CourseSerializer
        else:
            return CourseDetailSerializer

    def get_permissions(self):
        """
        Проверка прав в соответсвтии от метода обращения
        Любой авторизованный пользователь может создавать новый экземпляр
        Moder может только просматривать все курсы и не может создавать новые курсы
        Владец курса может просматривать/изменять/удалять только свои курсы
        """
        if self.action == 'create':
            self.permission_classes = (~IsModer,)
        elif self.action in ['update', 'partial_update', 'retrieve', 'list']:
            self.permission_classes = (IsOwner | IsModer,)
        elif self.action == 'destroy':
            self.permission_classes = (~IsModer | IsOwner,)
        return super().get_permissions()

    def perform_create(self, serializer):
        """
        Сохраняем созданный экземпляр Курса с владельцем текущего пользователя
        """
        course = serializer.save(owner=self.request.user)
        course.save()


########LESSON#########
class LessonCreateAPIView(generics.CreateAPIView):
    """
    Создаем новый Урок с владельцем, текущим, авторизованным пользователем
    Внутри сериализатора есть валидация для поля 'url'
    Moder не может создавать новые Уроки
    """
    serializer_class = LessonSerializer
    permission_classes = (~IsModer,)

    def perform_create(self, serializer):
        lesson = serializer.save(owner=self.request.user)
        lesson.save()


class LessonListAPIView(generics.ListAPIView):
    """
    Получаем список всех Уроков с владельцем, текущим, авторизованным пользователем
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = CustomPagination


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """
    Получаем детальную информацию о конкретном Уроке
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    """
    Изменяем информацию о конкретном Уроке
    Только владелец и Moder может изменять Урок
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsModer | IsOwner,)


class LessonDestroyAPIView(generics.DestroyAPIView):
    """
    Удаляем конкретный Урок
    Удалить урок может только владец
    """
    queryset = Lesson.objects.all()
    permission_classes = (~IsModer | IsOwner,)


########Subscription#########

class SubscriptionCreateAPIView(generics.CreateAPIView):
    """
    Создаем/Удаляем подписку на конкретный курс в одном POST запросе
    Если экземпляр существует, то его удаляем
    Если экземпляр не существует, то создаем
    """
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()

    def post(self, request, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course')
        course = get_object_or_404(Course, pk=course_id)
        subscription = Subscription.objects.filter(user=user, course=course)

        if subscription.exists():
            message = 'Подписка на курс '+str(course.title)+' отменена'
            subscription.delete()
        else:
            # Subscription.objects.create(user=user, course=course)
            message = 'Подписка на курс '+str(course.title)+' успешно оформлена'
        return Response({'message': message})
