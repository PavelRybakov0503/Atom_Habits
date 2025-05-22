from rest_framework import generics
from rest_framework.permissions import AllowAny

from habits.models import Habit
from habits.paginators import MyPagination
from habits.serializers import HabitSerializer
from habits.permissions import IsOwner


class HabitCreateAPIView(generics.CreateAPIView):
    """Эндпоинт создания привычки"""

    serializer_class = HabitSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HabitListAPIView(generics.ListAPIView):
    """Эндпоинт списка привычек"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = MyPagination

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class PublishedHabitListAPIView(generics.ListAPIView):
    """Эндпоинт списка публичных привычек"""

    queryset = Habit.objects.filter(is_published=True)
    serializer_class = HabitSerializer
    pagination_class = MyPagination
    permission_classes = (AllowAny,)


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """Эндпоинт просмотра привычки"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer


class HabitUpdateAPIView(generics.UpdateAPIView):
    """Эндпоинт изменения привычки"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = (IsOwner,)


class HabitDestroyAPIView(generics.DestroyAPIView):
    """Эндпоинт удаления привычки"""

    queryset = Habit.objects.all()
    permission_classes = (IsOwner,)
