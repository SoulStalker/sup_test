# Generated by Django 5.1.4 on 2025-02-21 19:26

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("models", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="date_created",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="Дата создания"
            ),
        ),
    ]
