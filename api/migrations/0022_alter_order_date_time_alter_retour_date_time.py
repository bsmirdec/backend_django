# Generated by Django 4.2.2 on 2023-09-04 06:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0021_alter_order_date_time_alter_retour_date_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="date_time",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 9, 5, 6, 55, 13, 663700, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="retour",
            name="date_time",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 9, 5, 6, 55, 13, 663700, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
