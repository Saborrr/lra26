from django.core.validators import MinValueValidator
from django.db import models


class Score(models.Model):
    team = models.ForeignKey(
        "teams.Team",
        on_delete=models.CASCADE,
        related_name="scores",
        verbose_name="Команда",
    )
    quest = models.ForeignKey(
        "quests.Quest",
        on_delete=models.CASCADE,
        related_name="scores",
        verbose_name="Квест",
    )
    points = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0)], verbose_name="Баллы"
    )
    verified = models.BooleanField(default=True, verbose_name="Подтверждён")
    entered_by = models.ForeignKey(
        "trainers.Trainer",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="entered_scores",
        verbose_name="Внёс",
    )
    notes = models.TextField(blank=True, max_length=1000, verbose_name="Примечания")
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "Результат"
        verbose_name_plural = "Результаты"
        constraints = [
            models.UniqueConstraint(fields=["team", "quest"], name="unique_team_quest_score"),
            models.CheckConstraint(
                condition=models.Q(points__gte=0), name="score_points_non_negative"
            ),
        ]

    def __str__(self):
        return f"{self.team} · {self.quest_id}: {self.points}"
