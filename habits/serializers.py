from rest_framework import serializers

from habits.models import HealthyHabit, PleasantHabit, Habit
from habits.validators import ValidateReward, ValidateTimeRequired, ValidateRewardForUpdate


class HealthyHabitSerializer(serializers.ModelSerializer):
    """
    Сериализатор для просмотра и получения полной информации о полезной привычке (HealthyHabit).
    Используется для вывода всех полей и не содержит дополнительных ограничений.
    """
    class Meta:
        model = HealthyHabit
        fields = "all"


class CreateHealthyHabitSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания новой полезной привычки (HealthyHabit).

    Исключает поле 'user', так как пользователь подставляется автоматически.
    В списке валидаторов:
        - ValidateTimeRequired: проверяет, что время выполнения привычки не превышает лимит.
        - ValidateReward: проверяет, что либо указана награда, либо связанная приятная привычка, но не оба поля
         одновременно.
    """
    class Meta:
        model = HealthyHabit
        exclude = ('user',)
        validators = [
            ValidateTimeRequired(time_required='time_required'),
            ValidateReward(reward='reward', related_habit='related_habit'),
        ]


class UpdateHealthyHabitSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления полезной привычки (HealthyHabit).

    В списке валидаторов:
        - ValidateTimeRequired: проверяет лимит по времени выполнения привычки.
        - ValidateRewardForUpdate: проверяет корректность полей награды и связанной приятной привычки.

    Также реализована валидация:
    - Если выбрана связанная привычка и есть награда, поле награды принудительно очищается.
    - Если выбрана награда и есть связанная привычка, поле связанной привычки принудительно очищается.
    """
    class Meta:
        model = HealthyHabit
        fields = "all"
        validators = [
            ValidateTimeRequired(
                time_required='time_required'
            ),
            ValidateRewardForUpdate(
                reward='reward',
                related_habit='related_habit'
            ),
        ]

    def validate(self, data):
        """
        Кастомная валидация полей 'reward' и 'related_habit':
        - Очищает одно из полей, если оба были заданы одновременно.
        """
        if 'related_habit' in dict(data) and data['related_habit'] and self.instance.reward:
            data['reward'] = None
            return data
        elif 'reward' in dict(data) and data['reward'] and self.instance.related_habit:
            data['related_habit'] = None
            return data
        else:
            return data


class PleasantHabitSerializer(serializers.ModelSerializer):
    """
    Сериализатор для просмотра и получения полной информации о приятной привычке (PleasantHabit).

    Использует валидатор ValidateTimeRequired для ограничения времени выполнения привычки.
    """
    class Meta:
        model = PleasantHabit
        fields = "all"
        validators = [
            ValidateTimeRequired(
                time_required='time_required'
            ),
        ]


class CreatePleasantHabitSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания приятной привычки (PleasantHabit).

    Исключает поле 'user', так как оно определяется автоматически.
    Использует валидатор ValidateTimeRequired для ограничения времени выполнения.
    """
    class Meta:
        model = PleasantHabit
        exclude = ('user',)
        validators = [
            ValidateTimeRequired(
                time_required='time_required'
            ),
        ]


class PublicHabitsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения публичных привычек (Habit).
    Отображает все поля базовой модели привычки.
    """
    class Meta:
        model = Habit
        fields = "all"
