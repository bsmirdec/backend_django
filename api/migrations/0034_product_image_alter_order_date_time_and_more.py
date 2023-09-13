# Generated by Django 4.2.2 on 2023-09-07 08:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0033_alter_order_date_time_alter_retour_date_time"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to=""),
        ),
        migrations.AlterField(
            model_name="order",
            name="date_time",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 9, 8, 8, 42, 57, 145864, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="retour",
            name="date_time",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 9, 8, 8, 42, 57, 145864, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
