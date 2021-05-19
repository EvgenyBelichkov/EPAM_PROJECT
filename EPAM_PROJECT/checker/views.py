import datetime

import requests
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render

from .models import WeatherStory

# Create your views here.


def main(request):
    return render(request, "checker/index.html")


def contacts(request):
    return render(request, "checker/contacts.html")


def checking_city_in_database(city_name):
    return WeatherStory.objects.filter(city_name=city_name).values()


def checking_city_in_database_test(city_name):
    return WeatherStory.objects.filter(city_name=city_name)


def insert_row(weather_dict):
    WeatherStory.objects.create(**weather_dict)


def update_row(city_name, weather_dict):
    WeatherStory.objects.filter(city_name=city_name).update(**weather_dict)


def get_weather_from_first_api(requested_city):
    first_api_url = "https://api.weatherbit.io/v2.0/current"
    params_for_first_api = {
        "city": requested_city,
        "key": "4f0f652aca7c4d64bb66902ea69e91aa",
        "units": "Metric",
    }
    result_from_first_api = requests.get(
        first_api_url, params_for_first_api
    ).json()  # noqa
    weather_from_first_api = {
        "current_temperature": result_from_first_api["data"][0]["temp"],
        "feels_like_temperature": result_from_first_api["data"][0]["app_temp"],
        "wind_speed": result_from_first_api["data"][0]["wind_spd"],
    }
    return weather_from_first_api


def get_weather_from_second_api(requested_city):
    second_api_url = "http://api.openweathermap.org/data/2.5/weather"
    params_for_second_api = {
        "q": requested_city,
        "appid": "11c0d3dc6093f7442898ee49d2430d20",
        "units": "metric",
    }
    result_from_second_api = requests.get(
        second_api_url, params_for_second_api
    ).json()  # noqa
    weather_from_second_api = {
        "current_temperature": result_from_second_api["main"]["temp"],
        "feels_like_temperature": result_from_second_api["main"]["feels_like"],
        "wind_speed": result_from_second_api["wind"]["speed"],
    }
    return weather_from_second_api


def union_api1_api2(requested_city, api1, api2):
    result_dict = {key: round((api1[key] + api2[key]) / 2, 2) for key in api1}
    result_dict["city_name"] = requested_city
    result_dict["time_created"] = datetime.datetime.now()
    return result_dict


def weather(request):
    requested_city = request.GET.get("request_city")
    city_check = checking_city_in_database(requested_city)

    if not city_check:
        source1 = get_weather_from_first_api(requested_city)
        source2 = get_weather_from_second_api(requested_city)
        result_dict = union_api1_api2(requested_city, source1, source2)
        insert_row(result_dict)
        return render(request, "checker/city.html", result_dict)

    if (
        datetime.datetime.now(datetime.timezone.utc)
        - city_check[0]["time_created"]  # noqa
    ) > settings.CURRENT_DURATION:
        source1 = get_weather_from_first_api(requested_city)
        source2 = get_weather_from_second_api(requested_city)
        result_dict = union_api1_api2(requested_city, source1, source2)
        update_row(requested_city, result_dict)
        return render(request, "checker/city.html", result_dict)

    else:
        return render(request, "checker/city.html", city_check[0])


def completed_requests(request):
    cities_list = WeatherStory.objects.all()
    paginator = Paginator(cities_list, 4)
    page_number = request.GET.get("page")
    try:
        page_cities = paginator.page(page_number)
    except PageNotAnInteger:
        page_cities = paginator.page(1)
    except EmptyPage:
        page_cities = paginator.page(paginator.num_pages)
    return render(
        request, "checker/cities_on_page.html", {"page_cities": page_cities}  # noqa
    )


def page_not_found(request, exception):
    return render(request, "checker/404.html")
