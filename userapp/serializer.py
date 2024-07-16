from rest_framework.serializers import ModelSerializer

from userapp.models import Payment, User


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

    def create(self, validated_data):
        payment = Payment.objects.create(**validated_data)
        return payment


class UserPaymentSerializer(ModelSerializer):
    payment = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'payment', 'email', 'is_staff']

    def create(self, validated_data):
        payments = validated_data.pop('payment')

        user = User.objects.create(**validated_data)
        for payment in payments:
            Payment.objects.create(user=user, **payment)
        return user


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'avatar', 'country', 'password']


class UserCensoredSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'avatar', 'country']
