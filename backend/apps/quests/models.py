from django.db import models


# Модель Квеста (Quest) - задания для команд.
# Отвечает за описание квестов, их баллы, статус.
# ID - строковый ключ (Q1, challenge-1), используется в Score.quest_id.
# Регулировать: добавить deadline, category, image, изменить PK на AutoField.
class Quest(models.Model):
    # Уникальный ID квеста (PK, строка)
    id = models.CharField(max_length=50, primary_key=True)
    # Название квеста
    title = models.CharField(max_length=200)
    # Описание/условия (опционально)
    description = models.TextField(blank=True)
    # Баллы за выполнение
    points = models.PositiveIntegerField()
    # Активен ли квест (для фильтра)
    active = models.BooleanField(default=True)
    # Дата создания
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]
        verbose_name = "Квест"
        verbose_name_plural = "Квесты"

    def __str__(self):
        return f"{self.id}: {self.title} ({self.points} pts)"
