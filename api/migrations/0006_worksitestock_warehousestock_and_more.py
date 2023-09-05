# Generated by Django 4.2.2 on 2023-08-23 07:13

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0005_category_product_type_worksitemaxproduct_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="WorksiteStock",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        db_index=True, default=django.utils.timezone.now
                    ),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("quantity", models.PositiveIntegerField()),
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
        migrations.CreateModel(
            name="WarehouseStock",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.IntegerField()),
                (
                    "product",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="api.product"
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="worksitestock",
            constraint=models.UniqueConstraint(
                fields=("worksite", "product"), name="unique_stock"
            ),
        ),
    ]
