from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

from Reception.views import add_room, add_client, room_reservation, fetch_rooms

urlpatterns = [
    path("", TemplateView.as_view(template_name="reception/reception_home.html"), name="home"),
    path('add_client/', add_client, name='add_client'),
    path('room_reservation/', room_reservation, name='room_reservation'),
    path('add_room/', add_room, name='add_room'),
    path('fetch_rooms/', fetch_rooms, name='fetch_rooms'),
]
