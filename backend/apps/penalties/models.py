from django.core.validators import MinValueValidator
from django.db import models


class BlackMark(models.Model):
    team = models.ForeignKey(
        "teams.Team",
        on_delete=models.CASCADE,
        related_name="black_marks",
        verbose_name="Команда",
    )
    reason = models.CharField(max_length=200, verbose_name="Причина")
    penalty = models.PositiveIntegerField(
        default=10, validators=[MinValueValidator(1)], verbose_name="Штраф (баллы)"
    )
    given_by = models.ForeignKey(
        "trainers.Trainer",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="given_marks",
        verbose_name="Выдал",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Чёрная метка"
        verbose_name_plural = "Чёрные метки"
        constraints = [
            models.CheckConstraint(condition=models.Q(penalty__gte=1), name="penalty_positive")
        ]

    def __str__(self):
        return f"{self.team}: -{self.penalty}"
