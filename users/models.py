from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    """
    Кастомная модель пользователя.

    Использует email как уникальное поле для аутентификации.
    Имеет дополнительное поле telegram для ссылки на Telegram-профиль пользователя
    и поле chat для хранения идентификатора чата Telegram.
    Поле username отключено.
    """
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    telegram = models.CharField(
        max_length=64,
        unique=True,
        verbose_name='Telegram',
        **NULLABLE
    )
    chat = models.IntegerField(
        unique=True,
        verbose_name='айди чата',
        **NULLABLE
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
