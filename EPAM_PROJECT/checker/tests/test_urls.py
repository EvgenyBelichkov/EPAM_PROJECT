from django.test import TestCase
from django.urls import resolve, reverse

from ..views import completed_requests, contacts, main, weather


class TestUrls(TestCase):
    def test_main_page_view_is_resolved(self):
        url = reverse("main")
        self.assertEqual(resolve(url).func, main)

    def test_weather_page_view_is_resolved(self):
        url = reverse("weather")
        self.assertEqual(resolve(url).func, weather)

    def test_contacts_page_view_is_resolved(self):
        url = reverse("contacts")
        self.assertEqual(resolve(url).func, contacts)

    def test_completed_requests_page_view_is_resolved(self):
        url = reverse("completed_requests")
        self.assertEqual(resolve(url).func, completed_requests)
