# Generated by Django 3.1.4 on 2021-05-18 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("checker", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="weatherstory",
            name="current_temperature",
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name="weatherstory",
            name="feels_like_temperature",
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name="weatherstory",
            name="wind_speed",
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
