# Generated by Django 4.2.2 on 2023-08-30 03:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0008_rename_line_id_orderline_order_line_id_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="notification",
            name="link",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="order",
            name="date_time",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 8, 31, 3, 0, 7, 509452, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("edition", "édition"),
                    ("validation", "en validation"),
                    ("send", "envoyée"),
                    ("confirmed", "confirmé"),
                    ("refused", "refusée"),
                ],
                default="edition",
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="retour",
            name="date_time",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 8, 31, 3, 0, 7, 509452, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="retour",
            name="status",
            field=models.CharField(
                choices=[
                    ("edition", "édition"),
                    ("validation", "en validation"),
                    ("send", "envoyée"),
                    ("confirmed", "confirmé"),
                    ("refused", "refusée"),
                ],
                default="edition",
                max_length=50,
            ),
        ),
    ]
