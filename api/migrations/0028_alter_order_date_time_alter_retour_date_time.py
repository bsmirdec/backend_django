# Generated by Django 4.2.2 on 2023-09-06 08:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0027_alter_order_date_time_alter_retour_date_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="date_time",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 9, 7, 8, 0, 20, 615120, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="retour",
            name="date_time",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 9, 7, 8, 0, 20, 615120, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]