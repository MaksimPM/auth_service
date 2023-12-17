from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['pk', 'first_name', 'phone', 'email', 'site', 'password']

    def create(self, validated_data):
        """Создает пользователя и устанавливает ему пароль"""

        instance = super().create(validated_data)
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

    def update(self, instance, validated_data):
        """Обновляет пользователя входящими данными и устанавливает ему пароль"""

        instance = super().update(instance, validated_data)
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
