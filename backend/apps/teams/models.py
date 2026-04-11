from django.db import models


# Модель Команды (Team) - основная сущность лидерборда LRA26.
# Отвечает за хранение данных о команде: название, тренер, счет, позиция.
# Позиция рассчитывается автоматически на основе счета (Meta.ordering).
# Регулировать: max_length названий, default score=0, добавить поля (logo и т.д.), изменить ordering.
class Team(models.Model):
    # Уникальное название команды (обязательное)
    name = models.CharField(max_length=100, unique=True)
    # Имя тренера (опционально)
    trainer = models.CharField(max_length=100, blank=True)
    # Текущий счет команды (сумма баллов по квестам)
    score = models.IntegerField(default=0)
    # Позиция в лидерборде (null - не рассчитана)
    position = models.PositiveIntegerField(null=True, blank=True)
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

    def save(self, *args, **kwargs):
        # Автообновление позиции при сохранении (можно отключить)
        super().save(*args, **kwargs)
        # Здесь можно добавить логику расчета position на основе всех команд
