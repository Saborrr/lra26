from django.db import models
from django.contrib.auth.models import User


# Модель Тренера (Trainer) - связывает пользователя с командой.
# Отвечает за хранение данных о тренере: имя, Telegram, телефон.
# Связь с User опциональна (тренер может не иметь аккаунта).
class Trainer(models.Model):
    # Связь с пользователем Django (опционально)
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        verbose_name="Пользователь"
    )
    # Имя тренера (обязательное)
    name = models.CharField(
        max_length=100, 
        verbose_name="Имя тренера"
    )
    # Telegram ID для бота (опционально, уникально)
    telegram_id = models.BigIntegerField(
        null=True, 
        blank=True, 
        unique=True,
        verbose_name="Telegram ID"
    )
    # Телефон для связи (опционально)
    phone = models.CharField(
        max_length=20, 
        blank=True,
        verbose_name="Телефон"
    )
    # Дата создания
    created_at = models.DateTimeField(auto_now_add=True)
    # Дата обновления
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Тренер"
        verbose_name_plural = "Тренеры"

    def __str__(self):
        return self.name