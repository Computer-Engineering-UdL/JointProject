from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from Reception.views import add_room, add_client, room_reservation, check_in_1, fetch_rooms, worker_home, cancel_reservation

urlpatterns = [
    path("", worker_home, name="worker_home"),
    path('add_client/', add_client, name='add_client'),
    path('room_reservation/', room_reservation, name='room_reservation'),
    path('add_room/', add_room, name='add_room'),
    path('check-in/', check_in_1, name='check_in'),
    path('fetch_rooms/', fetch_rooms, name='fetch_rooms'),
    path('cancel_reservation/', cancel_reservation, name='cancel_reservation'),
]
