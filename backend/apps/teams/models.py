from django.db import models


# Модель Команды (Team) - основная сущность лидерборда LRA26.
# Отвечает за хранение данных о команде: название, тренер, счет, позиция.
# Позиция рассчитывается автоматически на основе счета (Meta.ordering).
class Team(models.Model):
    # Уникальное название команды (обязательное)
    name = models.CharField(
        max_length=100, 
        unique=True,
        verbose_name="Название"
    )
    # Тренер команды (ForeignKey к Trainer)
    trainer = models.ForeignKey(
        'trainers.Trainer',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='teams',
        verbose_name="Тренер"
    )
    # Текущий счет команды (сумма баллов по квестам)
    score = models.IntegerField(
        default=0,
        verbose_name="Счёт"
    )
    # Штрафные баллы (сумма black_marks.penalty)
    penalty = models.IntegerField(
        default=0,
        verbose_name="Штраф"
    )
    # Позиция в лидерборде (null - не рассчитана)
    position = models.PositiveIntegerField(
        null=True, 
        blank=True,
        verbose_name="Позиция"
    )
    # Цвет команды (для UI)
    color = models.CharField(
        max_length=20, 
        blank=True,
        verbose_name="Цвет"
    )
    # Логотип команды
    logo = models.ImageField(
        upload_to='team_logos/',
        blank=True,
        null=True,
        verbose_name="Логотип"
    )
    # Дата создания
    created_at = models.DateTimeField(auto_now_add=True)
    # Дата последнего обновления счета
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Сортировка: сначала по позиции, затем по убыванию счета (лучшие сверху)
        ordering = ["position", "-score"]
        verbose_name = "Команда"
        verbose_name_plural = "Команды"

    def __str__(self):
        return f"{self.name} ({self.score} pts)"

    @property
    def total_score(self):
        """Итоговый счёт с учётом штрафов."""
        return self.score - self.penalty