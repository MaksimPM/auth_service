from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import UserRegister, UserListAPIView, UserDestroyAPIView

app_name = UsersConfig.name

router = routers.DefaultRouter()

urlpatterns = [
    path('', UserListAPIView.as_view(), name='users'),
    path('sign_up/', UserRegister.as_view(), name='user_register'),
    path('<int:pk>/delete/', UserDestroyAPIView.as_view(), name='user_delete'),

    path('sign_in/', TokenObtainPairView.as_view(), name='token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls
