from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema

from habits.models import HealthyHabit, PleasantHabit, Habit
from habits.paginators import HabitPaginator
from habits.permissions import IsOwner
from habits.serializers import (HealthyHabitSerializer, PleasantHabitSerializer,
    CreateHealthyHabitSerializer, UpdateHealthyHabitSerializer, PublicHabitsSerializer, CreatePleasantHabitSerializer)


@extend_schema(summary="Создать полезную привычку.")
class CreateHealthyHabitApiView(generics.CreateAPIView):
    """
    Представление для создания полезной привычки.

    Доступно только для аутентифицированных пользователей.
    При создании привычки автоматически присваивает текущего пользователя.
    """
    serializer_class = CreateHealthyHabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Метод вызывается при создании привычки.
        Присваивает полю user текущего пользователя.
        """
        new_habit = serializer.save()
        new_habit.user = self.request.user
        new_habit.save()


@extend_schema(summary="Получить список полезных привычек.")
class ListHealthyHabitApiView(generics.ListAPIView):
    """
    Представление для получения списка полезных привычек пользователя.

    Доступно только для аутентифицированных пользователей.
    Используется пагинация.
    """
    serializer_class = HealthyHabitSerializer
    queryset = HealthyHabit.objects.all()
    pagination_class = HabitPaginator
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Возвращает только полезные привычки текущего пользователя.
        """
        return PleasantHabit.objects.filter(user=self.request.user).order_by('pk')


@extend_schema(summary="Просмотреть полезную привычку.")
class RetrieveHealthyHabitApiView(generics.RetrieveAPIView):
    """
    Представление для получения одной полезной привычки по id.

    Доступно только для владельца привычки.
    """
    serializer_class = HealthyHabitSerializer
    queryset = HealthyHabit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


@extend_schema(summary="Редактировать полезную привычку.")
class UpdateHealthyHabitApiView(generics.UpdateAPIView):
    """
    Представление для редактирования полезной привычки.

    Доступно только для владельца привычки.
    """
    serializer_class = UpdateHealthyHabitSerializer
    queryset = HealthyHabit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


@extend_schema(summary="Удалить полезную привычку.")
class DestroyHealthyHabitApiView(generics.DestroyAPIView):
    """
    Представление для удаления полезной привычки.

    Доступно только для владельца привычки.
    """
    queryset = HealthyHabit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


@extend_schema(summary="Создать приятную привычку.")
class CreatePleasantHabitApiView(generics.CreateAPIView):
    """
    Представление для создания приятной привычки.

    Доступно только для аутентифицированных пользователей.
    При создании привычки автоматически присваивает текущего пользователя.
    """
    serializer_class = CreatePleasantHabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Метод вызывается при создании привычки.
        Присваивает полю user текущего пользователя.
        """
        new_habit = serializer.save()
        new_habit.user = self.request.user
        new_habit.save()


@extend_schema(summary="Получить список приятных привычек.")
class ListPleasantHabitApiView(generics.ListAPIView):
    """
    Представление для получения списка приятных привычек пользователя.

    Доступно только для аутентифицированных пользователей.
    Используется пагинация.
    """
    serializer_class = PleasantHabitSerializer
    queryset = PleasantHabit.objects.all()

    pagination_class = HabitPaginator
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Возвращает только приятные привычки текущего пользователя.
        """
        return PleasantHabit.objects.filter(user=self.request.user).order_by('pk')


@extend_schema(summary="Просмотреть приятную привычку.")
class RetrievePleasantHabitApiView(generics.RetrieveAPIView):
    """
    Представление для получения одной приятной привычки по id.

    Доступно только для владельца привычки.
    """
    serializer_class = PleasantHabitSerializer
    queryset = PleasantHabit.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]


@extend_schema(summary="Редактировать приятную привычку.")
class UpdatePleasantHabitApiView(generics.UpdateAPIView):
    """
    Представление для редактирования приятной привычки.

    Доступно только для владельца привычки.
    """
    serializer_class = PleasantHabitSerializer
    queryset = PleasantHabit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


@extend_schema(summary="Удалить приятную привычку.")
class DestroyPleasantHabitApiView(generics.DestroyAPIView):
    """
    Представление для удаления приятной привычки.

    Доступно только для владельца привычки.
    """
    queryset = PleasantHabit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


@extend_schema(summary="Получить список публичных привычек.")
class ListPublicHabitsApiView(generics.ListAPIView):
    """
    Представление для получения списка публичных привычек.

    Отображаются только привычки, помеченные как публичные.
    Доступно только для аутентифицированных пользователей.
    """
    serializer_class = PublicHabitsSerializer
    queryset = Habit.objects.filter(is_public=True)
    permission_classes = [IsAuthenticated]
