# Generated by Django 4.2.2 on 2023-08-21 09:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0004_order_return_alter_employee_manager"),
        ("authentication", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="employee",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="api.employee",
            ),
        ),
    ]
