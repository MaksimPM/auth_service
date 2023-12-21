from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.serializers import UserSerializer, PasswordRecoverySerializer, RequestPasswordRecoverySerializer, \
    AuthorizationSerializer
from users.tasks import send_email_task, send_password_reset_email


class UserRegister(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        try:
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            user.JWTToken = str(refresh.access_token)
            generated_password = User.objects.make_random_password()
            user.set_password(generated_password)
            user.save()
            send_email_task.delay(user.id, generated_password)
        except:
            name = serializer.validated_data.get('name')
            phone = serializer.validated_data.get('phone')
            email = serializer.validated_data.get('email')
            site = serializer.validated_data.get('site')
            if not name or not phone or not email or not site:
                return Response({"error": "заполните все обязательные поля"}, status.HTTP_400_BAD_REQUEST)


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserAuthorizationView(GenericAPIView):
    serializer_class = AuthorizationSerializer
    queryset = User.objects.all()

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            user.JWTToken = str(refresh.access_token)
            user.save()
            return Response({'access_token': user.JWTToken})
        else:
            return Response({"error": "Неверные учетные данные"}, status.HTTP_401_UNAUTHORIZED)


class RequestPasswordRecoveryView(APIView):
    serializer_class = RequestPasswordRecoverySerializer

    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            send_password_reset_email.delay(user.id)
            return Response({"message": "Письмо с ссылкой для сброса пароля отправлена на email"})
        except User.DoesNotExist:
            return Response({"message": "Пользователь не найден"}, status.HTTP_400_BAD_REQUEST)


class PasswordRecoveryView(generics.UpdateAPIView):
    serializer_class = PasswordRecoverySerializer
    queryset = User.objects.all()

    def update(self, request, *args, **kwargs):
        hash_value = kwargs.get('hash')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(password=hash_value)
        except User.DoesNotExist:
            return Response({"message": "Invalid hash"})
        new_password = serializer.validated_data.get('password')
        user.set_password(new_password)
        user.password_reset_hash = None
        user.save()

        refresh = RefreshToken.for_user(user)
        user.JWTToken = str(refresh.access_token)
        user.save()
        return Response({"message": "Пароль успешно обновлён!",
                         "access_token": user.JWTToken},
                        status.HTTP_200_OK)
