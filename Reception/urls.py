from django.urls import path
from django.views.generic import TemplateView
from Reception.views import (worker_home, add_client, room_reservation, add_room, check_in_1, fetch_rooms,
                             search_reservation, reservation_details, delete_reservation, check_in_summary,
                             print_receipt)


urlpatterns = [
    path("", worker_home, name="worker_home"),
    path("home/", TemplateView.as_view(template_name="worker/receptionist/receptionist_home.html"),
         name="receptionist_home"),
    path('add_client/', add_client, name='add_client'),
    path('room_reservation/', room_reservation, name='room_reservation'),
    path('add_room/', add_room, name='add_room'),
    path('check-in/', check_in_1, name='check_in'),
    path('check-in/summary/', check_in_summary, name='check_in_summary'),
    path('print_receipt/<int:client_id>/<int:reservation_id>/', print_receipt, name='print_receipt'),
    path('fetch_rooms/', fetch_rooms, name='fetch_rooms'),
    path('search_reservation/', search_reservation, name='search_reservation'),
    path('reservation_details/<int:pk>/', reservation_details, name='reservation_details'),
    path('reservation/delete/<int:pk>/', delete_reservation, name='delete_reservation'),
]
