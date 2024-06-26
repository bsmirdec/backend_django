# Generated by Django 4.2.2 on 2023-08-30 07:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0009_notification_link_alter_order_date_time_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="employee",
            name="threshold",
            field=models.IntegerField(
                choices=[(0, ""), (1, "courant"), (2, "important"), (3, "critique")],
                default=0,
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="date_time",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 8, 31, 7, 10, 34, 354777, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="retour",
            name="date_time",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 8, 31, 7, 10, 34, 354777, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
