# Generated by Django 4.2.2 on 2023-08-30 09:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0010_employee_threshold_alter_order_date_time_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employee",
            name="threshold",
            field=models.IntegerField(
                choices=[(0, ""), (1, "courant"), (2, "important"), (3, "critique")],
                default=0,
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="date_time",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 8, 31, 9, 30, 29, 725422, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="retour",
            name="date_time",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 8, 31, 9, 30, 29, 725422, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]