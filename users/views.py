from rest_framework import generics

from rest_framework_simplejwt.views import TokenObtainPairView

from drf_spectacular.utils import extend_schema

from users.serializers import RegistrationSerializer


@extend_schema(summary="Зарегистрироваться.")
class RegistrationApiView(generics.CreateAPIView):
    """
    Представление для регистрации нового пользователя.

    Позволяет создать нового пользователя с использованием сериализатора RegistrationSerializer.
    """

    serializer_class = RegistrationSerializer

    def perform_create(self, serializer):
        """
        Сохраняет нового пользователя и устанавливает ему пароль.

        Аргументы:
            serializer: Сериализатор данных пользователя.
        """
        new_user = serializer.save()
        new_user.set_password(new_user.password)
        new_user.save()


@extend_schema(summary="Войти.")
class AuthApiView(TokenObtainPairView):
    """
    Представление для аутентификации пользователя.

    Использует стандартную реализацию JWT-аутентификации.
    """
    pass
