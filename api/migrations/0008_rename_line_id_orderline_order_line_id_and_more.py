# Generated by Django 4.2.2 on 2023-08-28 09:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0007_orderline_retour_retourline_delete_return_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="orderline",
            old_name="line_id",
            new_name="order_line_id",
        ),
        migrations.RemoveField(
            model_name="retourline",
            name="line_id",
        ),
        migrations.AddField(
            model_name="retourline",
            name="id",
            field=models.BigAutoField(
                auto_created=True,
                default=12,
                primary_key=True,
                serialize=False,
                verbose_name="ID",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="order",
            name="date_time",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 8, 29, 9, 52, 6, 474686, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="retour",
            name="date_time",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 8, 29, 9, 52, 6, 474686, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
