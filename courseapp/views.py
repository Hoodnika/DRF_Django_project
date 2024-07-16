from rest_framework import viewsets, generics
from rest_framework.generics import get_object_or_404

from rest_framework.response import Response

from courseapp.models import Course, Lesson, Subscription
from courseapp.paginators import CustomPagination
from courseapp.serializer import CourseSerializer, LessonSerializer, CourseDetailSerializer, SubscriptionSerializer
from userapp.permissions import IsModer, IsOwner
from userapp.services import create_stripe_product

from courseapp.tasks import send_course_update_info


########_COURSE_#########
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
        create_stripe_product(course)
        course.save()

    def perform_update(self, serializer):
        course = serializer.save()
        send_course_update_info.delay(course.id)


########_LESSON_#########
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
        create_stripe_product(lesson)

        send_course_update_info.delay(lesson.course.id)
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

    # def perform_update(self, serializer):
    #     lesson = serializer.save()
    #     last_update_at = lesson.course.updated_at
    #
    #     send_course_update_info.delay(lesson.course.id)

    def partial_update(self, request, *args, **kwargs):
        lesson = self.get_object()
        serializer = self.get_serializer(lesson, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        send_course_update_info.delay(lesson.course.id)
        return Response(serializer.data)


class LessonDestroyAPIView(generics.DestroyAPIView):
    """
    Удаляем конкретный Урок
    Удалить урок может только владец
    """
    queryset = Lesson.objects.all()
    permission_classes = (~IsModer | IsOwner,)


########_Subscription_#########

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
            message = 'Подписка на курс ' + str(course.title) + ' отменена'
            subscription.delete()
        else:
            Subscription.objects.create(user=user, course=course)
            message = 'Подписка на курс ' + str(course.title) + ' успешно оформлена'
        return Response({'message': message})
