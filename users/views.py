from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from users.models import User
from users.permissions import IsOwnerProfile
from users.serializers import UserSerializer
from users.tasks import send_email_task


class UserRegister(generics.CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        send_email_task.delay(user.id)


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()


class UserDestroyAPIView(generics.DestroyAPIView):
    permission_classes = (AllowAny,)  # IsOwnerProfile,)
    queryset = User.objects.all()
