from django.db import models
from teams.models import Team


# Модель Счета (Score) - связывает команду и квест с баллами.
# Отвечает за запись результатов прохождения квестов командами.
# Сумма points по команде = team.score (обновляется вручную или сигналом).
# Регулировать: добавить verified, photo_proof, изменить ordering по timestamp.
class Score(models.Model):
    # Связь с командой (удаление счета при удалении команды)
    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="scores"
    )
    # ID квеста (строка для гибкости, e.g. 'Q1', 'challenge-1')
    quest_id = models.CharField(max_length=50)
    # Баллы за квест (default 0)
    points = models.IntegerField(default=0)
    # Время прохождения (авто)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Сортировка по новизне (последние сверху)
        ordering = ["-timestamp"]
        verbose_name = "Счет"
        verbose_name_plural = "Счета"

    def __str__(self):
        return f"{self.team.name} - {self.quest_id}: {self.points} pts"

    def save(self, *args, **kwargs):
        # После сохранения обновить team.score = sum(scores.points)
        super().save(*args, **kwargs)
        self.team.score = self.team.scores.aggregate(total=models.Sum('points'))['total'] or 0
        self.team.save(update_fields=['score'])
