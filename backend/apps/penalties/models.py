from django.db import models


# Модель Чёрной метки (BlackMark) - штрафы для команд.
# Отвечает за фиксацию нарушений и штрафных баллов.
# Сумма penalty по команде = team.penalty (обновляется через signal).
class BlackMark(models.Model):
    # Связь с командой
    team = models.ForeignKey(
        'teams.Team',
        on_delete=models.CASCADE,
        related_name="black_marks",
        verbose_name="Команда"
    )
    # Причина штрафа
    reason = models.CharField(
        max_length=200,
        verbose_name="Причина"
    )
    # Размер штрафа (в баллах)
    penalty = models.IntegerField(
        default=0,
        verbose_name="Штраф (баллы)"
    )
    # Кто выдал штраф (опционально)
    given_by = models.ForeignKey(
        'trainers.Trainer',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="given_marks",
        verbose_name="Выдал"
    )
    # Дата создания
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата"
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Чёрная метка"
        verbose_name_plural = "Чёрные метки"

    def __str__(self):
        return f"{self.team.name}: -{self.penalty} ({self.reason[:30]})"