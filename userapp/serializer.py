from rest_framework import serializers

from userapp.models import Payment, User


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        payments = validated_data.pop('payment')

        user = User.objects.create(**validated_data)
        for payment in payments:
            Payment.objects.create(user=user, **payment)
        return user
