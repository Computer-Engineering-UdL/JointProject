from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from Reception.views import add_room, add_client, new_reservation_1, check_in_1, fetch_rooms, worker_home, \
    new_reservation_2

urlpatterns = [
    path("", worker_home, name="worker_home"),
    path('add_client/', add_client, name='add_client'),
    path('new-reservation-1/', new_reservation_1, name='new_reservation_1'),
    path('new-reservation-2/', new_reservation_2, name='new_reservation_2'),
    path('add_room/', add_room, name='add_room'),
    path('check-in/', check_in_1, name='check_in'),
    path('fetch_rooms/', fetch_rooms, name='fetch_rooms'),
]
