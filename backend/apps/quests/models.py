from django.db import models


# Модель Квеста (Quest) - задания для команд.
# Отвечает за описание квестов, их баллы, статус.
# ID - строковый ключ (Q1, challenge-1), используется в Score.quest.
class Quest(models.Model):
    # Уникальный ID квеста (PK, строка)
    id = models.CharField(max_length=50, primary_key=True, verbose_name="ID")
    # Название квеста
    title = models.CharField(max_length=200, verbose_name="Название")
    # Описание/условия (опционально)
    description = models.TextField(blank=True, verbose_name="Описание")
    # Баллы за выполнение
    points = models.PositiveIntegerField(verbose_name="Баллы")
    # Категория квеста
    category = models.CharField(max_length=50, blank=True, verbose_name="Категория")
    # Порядок отображения
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    # Активен ли квест (для фильтра)
    active = models.BooleanField(default=True, verbose_name="Активен")
    # Дата создания
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Квест"
        verbose_name_plural = "Квесты"

    def __str__(self):
        return f"{self.id}: {self.title} ({self.points} pts)"
