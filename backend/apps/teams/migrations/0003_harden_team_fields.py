from django.core.validators import RegexValidator
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("teams", "0002_team_color_team_logo_team_penalty_alter_team_name_and_more")]

    operations = [
        migrations.AlterField(
            model_name="team",
            name="color",
            field=models.CharField(
                blank=True,
                default="#7c5cff",
                max_length=20,
                validators=[RegexValidator("^#[0-9a-fA-F]{6}$", "Используйте цвет #RRGGBB")],
                verbose_name="Цвет",
            ),
        ),
        migrations.AlterField(
            model_name="team",
            name="position",
            field=models.PositiveIntegerField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name="team",
            name="score",
            field=models.IntegerField(default=0, editable=False, verbose_name="Счёт"),
        ),
        migrations.AlterField(
            model_name="team",
            name="penalty",
            field=models.IntegerField(default=0, editable=False, verbose_name="Штраф"),
        ),
        migrations.AlterModelOptions(
            name="team",
            options={
                "ordering": ["name"],
                "verbose_name": "Команда",
                "verbose_name_plural": "Команды",
            },
        ),
    ]
