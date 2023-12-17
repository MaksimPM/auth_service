from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.permissions import IsOwnerProfile
from users.serializers import UserSerializer, PasswordRecoverySerializer, RequestPasswordRecoverySerializer
from users.tasks import send_email_task, send_password_reset_email


class UserRegister(generics.CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        send_email_task.delay(user.id)


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)  # IsAuthenticated,)
    queryset = User.objects.all()


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)  # IsAuthenticated, #IsOwnerProfile)
    queryset = User.objects.all()


class UserDestroyAPIView(generics.DestroyAPIView):
    permission_classes = (AllowAny,)  # IsOwnerProfile,)
    queryset = User.objects.all()


class UserAuthorizationView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = User.objects.get(email=email, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({'access_token': access_token})
        else:
            return Response({"error": "Неверные учетные данные"}, status.HTTP_401_UNAUTHORIZED)


class RequestPasswordRecoveryView(APIView):
    serializer_class = RequestPasswordRecoverySerializer

    def post(self, request):
        email = request.data.get('email')

        user = User.objects.get(email=email)
        send_password_reset_email.delay(user.id)
        return Response({"message": "Письмо с ссылкой для сброса пароля отправлена на email"})


class PasswordRecoveryView(generics.UpdateAPIView):
    serializer_class = PasswordRecoverySerializer

    def update(self, request, *args, **kwargs):
        hash_value = kwargs.get('hash')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(password=hash_value)
        except User.DoesNotExist:
            return Response({"message": "Invalid hash"}, status.HTTP_400_BAD_REQUEST)

        new_password = serializer.validated_data.get('new_password')
        user.set_password(new_password)
        user.password_reset_hash = None
        user.save()

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({"message": "Пароль успешно обновлён!",
                         "access_token": access_token},
                        status.HTTP_200_OK)
