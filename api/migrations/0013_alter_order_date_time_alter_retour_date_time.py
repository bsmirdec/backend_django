# Generated by Django 4.2.2 on 2023-08-31 11:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0012_remove_order_validation1_remove_order_validation2_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="date_time",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 9, 1, 11, 22, 39, 331296, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="retour",
            name="date_time",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 9, 1, 11, 22, 39, 331296, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
