from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['pk', 'name', 'phone', 'email', 'site', 'password', 'JWTToken']

    def validate_email(self, value):
        if User.objects.filter(email=value):
            raise serializers.ValidationError("Пользователь с таким email уже существует")
        return value

    def create(self, validated_data):
        instance = super().create(validated_data)
        return instance


class AuthorizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'email', 'password']


class PasswordRecoverySerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ['pk', 'password']


class RequestPasswordRecoverySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'email']
