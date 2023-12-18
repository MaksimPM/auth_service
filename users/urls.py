from django.urls import path
from rest_framework import routers

from users.apps import UsersConfig
from users.views import UserRegister, UserListAPIView, UserAuthorizationView, PasswordRecoveryView, \
    RequestPasswordRecoveryView

app_name = UsersConfig.name

router = routers.DefaultRouter()

urlpatterns = [
    path('', UserListAPIView.as_view(), name='users'),
    path('sign-up/', UserRegister.as_view(), name='user_register'),
    path('sign-in/', UserAuthorizationView.as_view(), name='user_authorization'),

    path('recovery/', RequestPasswordRecoveryView.as_view(), name='password_recovery'),
    path('recovery/<str:hash>/', PasswordRecoveryView.as_view(), name='password_recovery'),
] + router.urls
