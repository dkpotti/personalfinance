# Generated by Django 4.1.7 on 2023-04-21 20:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("expensetracker", "0002_unexpectedmonthlyexpense_expensestatus"),
    ]

    operations = [
        migrations.CreateModel(
            name="regularmonthlysavings",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("savingsName", models.CharField(max_length=50)),
                ("savingsAmount", models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
    ]