from django.db import models

from config import settings

NULLABLE = {'null': True, 'blank': True}


class Habit(models.Model):
    """
    Модель Habit хранит информацию о привычке пользователя.

    Атрибуты:
        user (ForeignKey): Ссылка на владельца привычки (пользователь).
        place (CharField): Место, где выполняется привычка.
        time (TimeField): Время для выполнения привычки.
        action (CharField): Описание действия привычки.
        regularity (CharField): Периодичность выполнения (ежедневно / ежемесячно).
        time_required (IntegerField): Сколько минут занимает привычка.
        is_public (BooleanField): Признак публичности привычки.
    """
    REGULARITY_CHOICES = (
        ('Daily', 'Eжедневно'),
        ('Monthly', 'Eжемесячно')
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='пользователь',
        **NULLABLE
    )
    place = models.CharField(max_length=255, verbose_name='место')
    time = models.TimeField(verbose_name='время, когда необходимо выполнять')
    action = models.CharField(max_length=255, verbose_name='действие')
    regularity = models.CharField(
        max_length=7,
        choices=REGULARITY_CHOICES,
        default='Daily',
        verbose_name='периодичность'
    )
    time_required = models.IntegerField(verbose_name='время на выполнение')
    is_public = models.BooleanField(
        default=False,
        verbose_name='признак публичности'
    )

    def str(self):
        """
        Возвращает строковое представление привычки.

        Returns:
            str: Описание действия привычки.
        """
        return f'{self.action}'


class PleasantHabit(Habit):
    """
    Модель PleasantHabit описывает приятные привычки пользователя.

    Наследует все поля базовой модели Habit.

    Используется для обозначения привычек, доставляющих пользователю удовольствие.
    """
    class Meta:
        verbose_name = 'Приятная привычка'
        verbose_name_plural = 'Приятные привычки'


class HealthyHabit(Habit):
    """
    Модель HealthyHabit описывает полезные привычки пользователя.

    Атрибуты (дополнительно к Habit):
        related_habit (ForeignKey): Ссылка на связанную приятную привычку.
        reward (CharField): Описание вознаграждения за выполнение полезной привычки.
    """
    related_habit = models.ForeignKey(
        PleasantHabit,
        on_delete=models.SET_NULL, **NULLABLE,
        verbose_name='связанная привычка'
    )
    reward = models.CharField(
        max_length=255,
        verbose_name='награда',
        **NULLABLE
    )

    class Meta:
        verbose_name = 'Полезная привычка'
        verbose_name_plural = 'Полезные привычки'
