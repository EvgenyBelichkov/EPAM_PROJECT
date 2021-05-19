import datetime
import time

from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from ..models import WeatherStory
from ..views import insert_row, union_api1_api2, update_row, weather


class LogicTestCase(TestCase):
    example_dict_1 = {
        "city_name": "Omsk",
        "current_temperature": 25,
        "feels_like_temperature": 30,
        "wind_speed": 2,
        "time_created": datetime.datetime(2021, 5, 18),
    }

    example_dict_2 = {
        "city_name": "Omsk",
        "current_temperature": 30,
        "feels_like_temperature": 35,
        "wind_speed": 7,
        "time_created": datetime.datetime(2021, 5, 19),
    }

    def set_up(self):
        self.client = Client()

    def test_counting_average_mean_of_weather_example_1(self):
        weather_from_api1 = {"temp": 1, "feels_like": 1, "wind_speed": 1}
        weather_from_api2 = {"temp": 2, "feels_like": 2, "wind_speed": 2}
        result = union_api1_api2("Omsk", weather_from_api1, weather_from_api2)
        expected_temp = 1.5
        expected_feels_like_temp = 1.5
        expected_wind_speed = 1.5
        self.assertEqual(result["temp"], expected_temp)
        self.assertEqual(result["feels_like"], expected_feels_like_temp)
        self.assertEqual(result["wind_speed"], expected_wind_speed)

    def test_counting_average_mean_of_weather_example_2(self):
        weather_from_api1 = {"temp": 0, "feels_like": 0, "wind_speed": 0}
        weather_from_api2 = {"temp": 0, "feels_like": 0, "wind_speed": 0}
        result = union_api1_api2("Omsk", weather_from_api1, weather_from_api2)
        expected_temp = 0
        expected_feels_like_temp = 0
        expected_wind_speed = 0
        self.assertEqual(result["temp"], expected_temp)
        self.assertEqual(result["feels_like"], expected_feels_like_temp)
        self.assertEqual(result["wind_speed"], expected_wind_speed)

    def test_response_200_and_used_template_on_main_page(self):
        url = reverse("main")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "checker/index.html")

    def test_response_200_and_used_template_on_weather_page(self):
        url = reverse("weather")
        response = self.client.get(url, {"request_city": "Kirov"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "checker/city.html")

    def test_response_200_and_used_template_on_completed_requests_page(self):
        url = reverse("completed_requests")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "checker/cities_on_page.html")

    def test_response_200_and_used_template_on_contact_page(self):
        url = reverse("contacts")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "checker/contacts.html")

    def test_inserting_rows(self):

        insert_row(LogicTestCase.example_dict_1)
        result_1 = WeatherStory.objects.count()
        expected_result_1 = 1
        insert_row(LogicTestCase.example_dict_2)
        result_2 = WeatherStory.objects.count()
        expected_result_2 = 2
        self.assertEqual(result_1, expected_result_1)
        self.assertEqual(result_2, expected_result_2)

    def test_updating_rows(self):
        insert_row(LogicTestCase.example_dict_1)
        update_row("Omsk", LogicTestCase.example_dict_2)
        result_row = WeatherStory.objects.filter(city_name="Omsk").values()
        self.assertEqual(result_row[0]["current_temperature"], 30)
        self.assertEqual(result_row[0]["feels_like_temperature"], 35)
        self.assertEqual(result_row[0]["wind_speed"], 7)

    def test_updating_function_that_checks_time(self):
        factory = RequestFactory()
        url = reverse("weather")
        request = factory.get(url, {"request_city": "Omsk"})

        weather(request)
        row_information = WeatherStory.objects.filter(city_name="Omsk")
        time_created = row_information.values()[0]["time_created"]

        weather(request)
        updated_row_information = WeatherStory.objects.filter(
            city_name="Omsk"
        ).values()[0]
        updated_time_created = updated_row_information["time_created"]
        self.assertEqual(time_created, updated_time_created)

        time.sleep(11)
        weather(request)
        new_updated_row_information = WeatherStory.objects.filter(
            city_name="Omsk"
        ).values()[0]
        new_updated_time_created = new_updated_row_information["time_created"]
        self.assertNotEqual(time_created, new_updated_time_created)
