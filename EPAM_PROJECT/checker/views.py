import datetime

import requests
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render

from .models import WeatherStory

# Create your views here.


def main(request):
    """This function showing the main page of the website"""
    return render(request, "checker/index.html")


def contacts(request):
    """The function represent contact information about developer"""
    return render(request, "checker/contacts.html")


def checking_city_in_database(city_name):
    """The function checks information about the requested
    city in the database"""
    return WeatherStory.objects.filter(city_name=city_name).values()


def insert_row(weather_dict):
    """The function that inserts information about the city
    in the database if there is no information"""
    WeatherStory.objects.create(**weather_dict)


def update_row(city_name, weather_dict):
    """The function that updated information about the city
    in the database, if information not actual"""
    WeatherStory.objects.filter(city_name=city_name).update(**weather_dict)


def get_weather_from_first_api(requested_city):
    """Taking information about the weather in the requested
     city using API service 'weatherbit'. The function returns
    information in dictionary"""
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
    """Taking information about the weather in the requested
    city using API service 'openweathermap'. The function returns
    information in dictionary"""
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
    """The function union results from two different API services"""
    result_dict = {key: round((api1[key] + api2[key]) / 2, 2) for key in api1}
    result_dict["city_name"] = requested_city
    result_dict["time_created"] = datetime.datetime.now()
    return result_dict


def weather(request):
    """The function getting request from client (requested city)
    and collecting information in the next algorithm
    1) Checking city in database. If the city is in the database - the
     function checks relevance weather information. If not - getting
      repeated request;
    2) If the city isn't in database - function getting request;
    3) If information about the requested city is relevant in the
     database - client would get the weather from the database.
    """
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
    """Function that represents all complited requests on web-site.
    User would see last n results, that regulated in local settings."""
    cities_list = WeatherStory.objects.all()
    paginator = Paginator(cities_list, settings.NUMBER)
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


def page_not_found_500(request):
    return render(request, "checker/500.html")
