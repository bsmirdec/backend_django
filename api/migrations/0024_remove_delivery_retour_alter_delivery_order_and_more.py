# Generated by Django 4.2.2 on 2023-09-04 09:45

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0023_alter_order_date_time_alter_retour_date_time"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="delivery",
            name="retour",
        ),
        migrations.AlterField(
            model_name="delivery",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="api.order"
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="date_time",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 9, 5, 9, 44, 36, 427677, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="retour",
            name="date_time",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 9, 5, 9, 44, 36, 427677, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]