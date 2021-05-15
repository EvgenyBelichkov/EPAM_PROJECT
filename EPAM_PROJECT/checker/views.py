import datetime
import sqlite3
from contextlib import contextmanager

import requests
from django.shortcuts import render

# Create your views here.


def main(request):
    return render(request, "checker/index.html")


def contacts(request):
    return render(request, "checker/contacts.html")


@contextmanager
def connection(database_name):
    con = sqlite3.connect(database_name)
    yield con.cursor()
    con.commit()
    con.close()


def checking_city_in_database(database_name, table_name, city):
    with connection(database_name) as cursor:
        cursor.execute(
            f"SELECT * from {table_name} where city_name=:city ", {"city": city}  # noqa
        )
        # cursor.execute(f'DELETE FROM {table_name}')
        # cursor.execute(f'delete from sqlite_sequence where name=:table_name',{'table_name': table_name}) # noqa
        return cursor.fetchone()


def insert_row(
    database_name, table_name, city_name, temp, f_l_temp, wind_speed
):  # noqa
    with connection(database_name) as cursor:
        cursor.execute(
            f"INSERT INTO {table_name}(city_name, current_temperature, "
            f"feels_like_temperature, wind_speed, time_created ) "
            f"VALUES(?, ?, ?, ?, ?)",
            (city_name, temp, f_l_temp, wind_speed, datetime.datetime.now()),
        )


def update_row(
    database_name, table_name, city_name, temp, f_l_temp, wind_speed
):  # noqa
    with connection(database_name) as cursor:
        cursor.execute(
            f"UPDATE {table_name} set current_temperature = ?, "
            f"feels_like_temperature = ?, wind_speed = ?, "
            f"time_created = ? WHERE city_name = ?",
            (temp, f_l_temp, wind_speed, datetime.datetime.now(), city_name),
        )


def api_1(name_city):
    api_url = "https://api.weatherbit.io/v2.0/current"
    params = {
        "city": name_city,
        "key": "4f0f652aca7c4d64bb66902ea69e91aa",
        "units": "Metric",
    }
    weather_conditions = requests.get(api_url, params).json()
    requested_params = {
        "temp": weather_conditions["data"][0]["temp"],
        "feels_like": weather_conditions["data"][0]["app_temp"],
        "wind_speed": weather_conditions["data"][0]["wind_spd"],
    }
    return requested_params


def api_2(name_city):
    api_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": name_city,
        "appid": "11c0d3dc6093f7442898ee49d2430d20",
        "units": "metric",
    }
    weather_conditions = requests.get(api_url, params).json()
    requested_params = {
        "temp": weather_conditions["main"]["temp"],
        "feels_like": weather_conditions["main"]["feels_like"],
        "wind_speed": weather_conditions["wind"]["speed"],
    }
    return requested_params


def union_api1_api2(requested_city):
    data_1 = api_1(requested_city)
    data_2 = api_2(requested_city)
    result_dict = {
        "temp": round(float((data_1["temp"] + data_2["temp"]) / 2), 1),
        "feels_like": round(
            float((data_1["feels_like"] + data_2["feels_like"]) / 2), 1
        ),
        "wind_speed": round(
            float((data_1["wind_speed"] + data_2["wind_speed"]) / 2), 1
        ),
    }
    return result_dict


def weather(request):
    requested_city = request.GET["request_city"]
    city_check = checking_city_in_database(
        "db.sqlite3", "checker_weatherstory", requested_city
    )
    if not city_check:
        result_dict = union_api1_api2(requested_city)
        insert_row(
            "db.sqlite3",
            "checker_weatherstory",
            requested_city,
            result_dict["temp"],
            result_dict["feels_like"],
            result_dict["wind_speed"],
        )
        return render(request, "checker/city.html", result_dict)

    if datetime.datetime.now() - datetime.datetime.strptime(
        city_check[5], "%Y-%m-%d %H:%M:%S.%f"
    ) > datetime.timedelta(seconds=60):
        result_dict = union_api1_api2(requested_city)
        update_row(
            "db.sqlite3",
            "checker_weatherstory",
            requested_city,
            result_dict["temp"],
            result_dict["feels_like"],
            result_dict["wind_speed"],
        )
        return render(request, "checker/city.html", result_dict)
    else:
        result_dict = {
            "temp": city_check[2],
            "feels_like": city_check[3],
            "wind_speed": city_check[4],
        }
        return render(request, "checker/city.html", result_dict)
