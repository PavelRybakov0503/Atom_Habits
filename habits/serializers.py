from rest_framework import serializers

from .models import Habit
from .validators import (
    AssociatedWithoutRewardValidator,
    TimeToCompleteValidator,
    PleasantHabitRelatedValidator,
    PleasantHabitWithoutReward,
    PeriodicityValidator,
)


class HabitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habit
        fields = "__all__"
        validators = [
            AssociatedWithoutRewardValidator(field1="related_habit", field2="reward"),
            TimeToCompleteValidator(field1="time_to_complete"),
            PleasantHabitRelatedValidator(
                field1="related_habit", field2="pleasant_habit"
            ),
            PleasantHabitWithoutReward(
                field1="pleasant_habit", field2="reward", field3="related_habit"
            ),
            PeriodicityValidator(field1="periodicity"),
        ]