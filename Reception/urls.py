from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from Reception.views import add_room, add_client, room_reservation, check_in_1, fetch_rooms, worker_home, send_data, check_in_summary

urlpatterns = [
    path("", worker_home, name="worker_home"),
    path('add_client/', add_client, name='add_client'),
    path('room_reservation/', room_reservation, name='room_reservation'),
    path('add_room/', add_room, name='add_room'),
    path('check_in/', check_in_1, name='check_in'),
    path('check_in/send_data/', send_data,
         name='send_data'),
    path('check_in/summary/', check_in_summary, name='check_in_summary'),
    path('fetch_rooms/', fetch_rooms, name='fetch_rooms'),
]
