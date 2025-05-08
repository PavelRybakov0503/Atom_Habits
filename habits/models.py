from django.db import models
from rest_framework.exceptions import ValidationError

from users.models import User

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

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', **NULLABLE,
                             help_text='Пользователь - создатель привычки')
    place = models.CharField(max_length=255, verbose_name='место',
                             help_text='Место — место, в котором необходимо выполнять привычку.')
    time = models.TimeField(verbose_name='время, когда необходимо выполнять',
                            help_text='Время — время, когда необходимо выполнять привычку.')
    action = models.TextField(max_length=255, verbose_name='действие',
                              help_text='Действие — действие, которое, представляет из себя, привычка.')
    pleasant_habit = models.BooleanField(default=False, verbose_name='Признак приятной привычки',
                                         help_text='Признак приятной привычки — привычка, '
                                                   'которую можно привязать к выполнению полезной привычки.')
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='Связанная привычка',
                                      **NULLABLE,
                                      help_text='Связанная привычка — привычка, которая связана с другой привычкой, '
                                                'важно указывать для полезных привычек, но не для приятных.')
    regularity = models.CharField(
        max_length=7,
        choices=REGULARITY_CHOICES,
        default='Daily',
        verbose_name='периодичность'
    )
    reward = models.TextField(verbose_name='Вознаграждение за выполнение действия', **NULLABLE,
                              help_text='Вознаграждение — чем пользователь должен себя вознаградить после выполнения.')
    time_required = models.IntegerField(verbose_name='время на выполнение')
    is_public = models.BooleanField(
        default=False,
        verbose_name='признак публичности'
    )

    def __str__(self):
        if self.reward:
            reward = self.reward
        elif self.related_habit:
            reward = self.related_habit.action
        else:
            reward = 'Ты - свой самый лучший проект'
        return f'Я буду делать {self.action} в {self.time}, ' \
               f'\nместо: {self.place}' \
               f'\nНаграда: {reward}'

    def save(self, *args, **kwargs):
        """ Проверки выполнения привычки (должно быть не более 120 секунд) """

        if self.time_to_complete and self.time_to_complete > 120:
            raise ValidationError('Время выполнения привычки должно быть больше 0 и меньше 120 секунд!')
        return super().save(**kwargs)

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ('pk',)
