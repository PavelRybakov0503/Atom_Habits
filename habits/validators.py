from rest_framework.exceptions import ValidationError


class AssociatedWithoutRewardValidator:
    """Исключает одновременный выбор связанной привычки и указания вознаграждения"""

    def __init__(self, field1, field2):
        self.field1 = field1
        self.field2 = field2

    def __call__(self, instance):
        if instance.get(self.field1) and instance.get(self.field2):
            raise ValidationError(
                "Выбрана связанная привычка и указано вознаграждение."
                "Укажите либо связанную привычку, либо укажите вознаграждение."
            )


class TimeToCompleteValidator:
    """Исключает выбор времени на выполнение привычки, которое превышает 120 секунд"""

    duration = 120

    def __init__(self, field1):
        self.field1 = field1

    def __call__(self, instance):
        if instance.get(self.field1):
            if instance.get(self.field1) > self.duration:
                raise ValidationError(
                    "Указанное время на выполнение привычки превышает 120 секунд."
                )


class PleasantHabitRelatedValidator:
    """В связанные привычки могут попадать только привычки с признаком приятной привычки."""

    def __init__(self, field1, field2):
        self.field1 = field1
        self.field2 = field2

    def __call__(self, instance):
        if instance.get(self.field1):
            if not instance.get(self.field2):
                raise ValidationError(
                    "У связанной привычки должен быть указан признак приятной привычки."
                )


class PleasantHabitWithoutReward:
    """Исключает одновременный выбор связанной привычки и указания вознаграждения"""

    def __init__(self, field1, field2, field3):
        self.field1 = field1
        self.field2 = field2
        self.field3 = field3

    def __call__(self, instance):
        if instance.get(self.field1):
            if instance.get(self.field2) or instance.get(self.field3):
                raise ValidationError(
                    "У приятной привычки не может быть вознаграждения или связанной привычки."
                )


class PeriodicityValidator:
    """Исключает выбор периодичности привычки, которая превышает 7 дней"""

    def __init__(self, field1):
        self.field1 = field1

    def __call__(self, instance):
        periodicity = instance.get(self.field1)
        if periodicity:
            if periodicity > 7:
                raise ValidationError(
                    "Нельзя выполнять привычку реже, чем 1 раз в 7 дней."
                )
