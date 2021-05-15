from django.db import models

# Create your models here.


class WeatherStory(models.Model):
    city_name = models.CharField(max_length=250)
    current_temperature = models.IntegerField()
    feels_like_temperature = models.IntegerField()
    wind_speed = models.IntegerField()
    time_created = models.DateTimeField()
