import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("scores", "0002_alter_score_options_score_entered_by_score_notes_and_more")]

    operations = [
        migrations.AddField(
            model_name="score", name="updated_at", field=models.DateTimeField(auto_now=True)
        ),
        migrations.AlterField(
            model_name="score",
            name="points",
            field=models.PositiveIntegerField(
                default=0,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name="Баллы",
            ),
        ),
        migrations.AlterField(
            model_name="score",
            name="notes",
            field=models.TextField(blank=True, max_length=1000, verbose_name="Примечания"),
        ),
        migrations.AlterField(
            model_name="score",
            name="verified",
            field=models.BooleanField(default=True, verbose_name="Подтверждён"),
        ),
        migrations.AlterUniqueTogether(name="score", unique_together=set()),
        migrations.AddConstraint(
            model_name="score",
            constraint=models.UniqueConstraint(
                fields=("team", "quest"), name="unique_team_quest_score"
            ),
        ),
        migrations.AddConstraint(
            model_name="score",
            constraint=models.CheckConstraint(
                condition=models.Q(("points__gte", 0)), name="score_points_non_negative"
            ),
        ),
        migrations.AlterModelOptions(
            name="score",
            options={
                "ordering": ["-updated_at"],
                "verbose_name": "Результат",
                "verbose_name_plural": "Результаты",
            },
        ),
    ]
