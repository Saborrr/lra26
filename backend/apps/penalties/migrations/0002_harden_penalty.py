import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("penalties", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="blackmark",
            name="penalty",
            field=models.PositiveIntegerField(
                default=10,
                validators=[django.core.validators.MinValueValidator(1)],
                verbose_name="Штраф (баллы)",
            ),
        ),
        migrations.AddConstraint(
            model_name="blackmark",
            constraint=models.CheckConstraint(
                condition=models.Q(("penalty__gte", 1)), name="penalty_positive"
            ),
        ),
    ]
