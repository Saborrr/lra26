from django.core.validators import RegexValidator
from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    trainer = models.ForeignKey(
        "trainers.Trainer",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="teams",
        verbose_name="Тренер",
    )
    score = models.IntegerField(default=0, editable=False, verbose_name="Счёт")
    penalty = models.IntegerField(default=0, editable=False, verbose_name="Штраф")
    position = models.PositiveIntegerField(null=True, blank=True, editable=False)
    color = models.CharField(
        max_length=20,
        blank=True,
        default="#7c5cff",
        validators=[RegexValidator(r"^#[0-9a-fA-F]{6}$", "Используйте цвет #RRGGBB")],
        verbose_name="Цвет",
    )
    logo = models.ImageField(upload_to="team_logos/", blank=True, null=True, verbose_name="Логотип")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Команда"
        verbose_name_plural = "Команды"

    def __str__(self):
        return self.name

    @property
    def total_score(self):
        return self.score - self.penalty
