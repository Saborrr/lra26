from django.db import models
from apps.teams.models import Team


# Модель Счета (Score) - связывает команду и квест с баллами.
# Отвечает за запись результатов прохождения квестов командами.
# Сумма points по команде = team.score (обновляется через signal).
class Score(models.Model):
    # Связь с командой (удаление счета при удалении команды)
    team = models.ForeignKey(
        Team, 
        on_delete=models.CASCADE, 
        related_name="scores",
        verbose_name="Команда"
    )
    # Связь с квестом (ForeignKey вместо CharField)
    quest = models.ForeignKey(
        'quests.Quest',
        on_delete=models.CASCADE,
        related_name="scores",
        verbose_name="Квест"
    )
    # Баллы за квест (default 0)
    points = models.IntegerField(
        default=0,
        verbose_name="Баллы"
    )
    # Подтверждён ли результат
    verified = models.BooleanField(
        default=False,
        verbose_name="Подтверждён"
    )
    # Кто внёс результат
    entered_by = models.ForeignKey(
        'trainers.Trainer',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="entered_scores",
        verbose_name="Внёс"
    )
    # Примечания
    notes = models.TextField(
        blank=True,
        verbose_name="Примечания"
    )
    # Время прохождения (авто)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Сортировка по новизне (последние сверху)
        ordering = ["-timestamp"]
        verbose_name = "Результат"
        verbose_name_plural = "Результаты"
        # Уникальность: одна команда - один квест
        unique_together = ['team', 'quest']

    def __str__(self):
        return f"{self.team.name} - {self.quest_id}: {self.points} pts"