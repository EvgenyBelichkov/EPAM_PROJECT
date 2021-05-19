from django.db import models

# Create your models here.


class WeatherStory(models.Model):
    city_name = models.CharField(max_length=250)
    current_temperature = models.DecimalField(max_digits=5, decimal_places=2)
    feels_like_temperature = models.DecimalField(max_digits=5, decimal_places=2)  # noqa
    wind_speed = models.DecimalField(max_digits=5, decimal_places=2)
    time_created = models.DateTimeField()

    def __str__(self):
        return self.city_name
