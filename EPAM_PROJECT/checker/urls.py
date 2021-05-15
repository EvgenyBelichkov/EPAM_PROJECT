from django.urls import path

from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path("weather", views.weather, name="weather"),
    path("contacts", views.contacts, name="contacts"),
]
