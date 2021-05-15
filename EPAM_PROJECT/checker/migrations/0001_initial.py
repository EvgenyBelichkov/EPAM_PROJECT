# Generated by Django 3.1.4 on 2021-05-14 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="WeatherStory",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("city_name", models.CharField(max_length=250)),
                ("current_temperature", models.IntegerField()),
                ("feels_like_temperature", models.IntegerField()),
                ("wind_speed", models.IntegerField()),
                ("time_created", models.DateTimeField()),
            ],
        ),
    ]