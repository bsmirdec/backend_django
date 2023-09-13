# Generated by Django 4.2.2 on 2023-09-06 07:52

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0025_stock_alter_order_date_time_alter_retour_date_time_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="WorksiteMaxStock",
            fields=[
                (
                    "created_at",
                    models.DateTimeField(
                        db_index=True, default=django.utils.timezone.now
                    ),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("quantity", models.PositiveIntegerField()),
                ("max_stock_id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.product"
                    ),
                ),
                (
                    "worksite",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.worksite"
                    ),
                ),
            ],
        ),
        migrations.AlterField(
            model_name="order",
            name="date_time",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 9, 7, 7, 52, 19, 835422, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="retour",
            name="date_time",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 9, 7, 7, 52, 19, 835422, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.DeleteModel(
            name="WorksiteMaxProduct",
        ),
        migrations.AddConstraint(
            model_name="worksitemaxstock",
            constraint=models.UniqueConstraint(
                fields=("worksite", "product"), name="unique_max_stock"
            ),
        ),
    ]
