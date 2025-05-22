from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="Email", help_text="Введите Email"
    )
    city = models.CharField(
        max_length=20,
        verbose_name="Город",
        help_text="Введите город проживания",
        blank=True,
        null=True,
    )
    avatar = models.ImageField(
        upload_to="users/avatars", verbose_name="Аватар", blank=True, null=True
    )
    tg_chat_id = models.CharField(
        max_length=50,
        verbose_name="Chat-ID Telegram",
        help_text="Введите Chat-ID Telegram",
        blank=True,
        null=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
