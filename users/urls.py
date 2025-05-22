from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.apps import UsersConfig
from users.views import (
    UserCreateAPIView,
    UserRetrieveAPIView,
    UserUpdateAPIView,
    UserDestroyAPIView,
)

app_name = UsersConfig.name

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register-user"),
    path("<int:pk>/", UserRetrieveAPIView.as_view(), name="user-detail"),
    path("<int:pk>/update/", UserUpdateAPIView.as_view(), name="user-update"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("<int:pk>/delete/", UserDestroyAPIView.as_view(), name="delete"),
]
