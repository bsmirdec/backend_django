# Generated by Django 4.2.2 on 2023-08-17 07:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="worksite",
            name="client",
            field=models.CharField(default="Ma Bite", max_length=50),
            preserve_default=False,
        ),
    ]
