from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny

from courseapp.paginators import CustomPagination
from userapp.models import Payment, User
from userapp.permissions import IsMe, IsModer
from userapp.serializer import PaymentSerializer, UserPaymentSerializer, UserSerializer, UserCensoredSerializer
from userapp.services import create_stripe_price, create_stripe_session


########_PAYMENT_############
class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_type')
    ordering_fields = ('datetime_payment',)
    permission_classes = (IsModer,)


class PaymentCreateAPIView(generics.CreateAPIView):
    """
    Создаем новую оплату, с владельцем, текущим, авторизованным пользователем
    """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(owner=self.request.user)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data.get('paid_lesson'):
            lesson = serializer.validated_data.get('paid_lesson')
            price = lesson.price
            price_stripe = create_stripe_price(price, lesson.title)
        elif serializer.validated_data.get('paid_course'):
            course = serializer.validated_data.get('paid_course')
            price = sum(lesson.price for lesson in course.lesson.all())
            price_stripe = create_stripe_price(price, course.title)
        else:
            raise ValueError("Не указан paid_lesson или paid_course")
        payment.price = price
        session_id, link = create_stripe_session(price_stripe)
        payment.session_id = session_id
        payment.link = link
        payment.save()


def payment_success(request):
    context = {}
    return render(request, 'userapp/payment_success.html', context)


########_USER_############
class UserListAPIView(generics.ListAPIView):
    """
    Получаем список всех пользователей
    Доступно только для Moder
    """
    serializer_class = UserCensoredSerializer
    queryset = User.objects.all()
    pagination_class = CustomPagination
    permission_classes = (IsModer,)


class UserCreateAPIView(generics.CreateAPIView):
    """
    'API endpoint' для регистрации
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """
    Получаем детальную информацию о конкретном пользователе
    Доступно только для текущего пользователя и Moder
    """
    serializer_class = UserPaymentSerializer
    queryset = User.objects.all()
    permission_classes = (IsModer | IsMe,)


class UserUpdateAPIView(generics.UpdateAPIView):
    """
    Изменяем информацию о конкретном пользователе
    Пользватель может изменять только свой профиль
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsMe,)


class UserDestroyAPIView(generics.DestroyAPIView):
    """
    Удаляем конкретного пользователя
    Пользватель может удалять только свой профиль
    """
    queryset = User.objects.all()
    permission_classes = (IsMe,)
