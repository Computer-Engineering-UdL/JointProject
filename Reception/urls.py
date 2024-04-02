from django.urls import path
from django.views.generic import TemplateView
from Reception import views as v

urlpatterns = [
    path("", v.worker_home, name="worker_home"),
    path("home/", TemplateView.as_view(template_name="worker/receptionist/receptionist_home.html"),
         name="receptionist_home"),
    path('add_client', v.add_client, name='add_client'),
    path('room_reservation/', v.room_reservation, name='room_reservation'),
    path('add_room/', v.add_room, name='add_room'),
    path('check-in/', v.check_in_1, name='check_in'),
    path('check-in/summary/', v.check_in_summary, name='check_in_summary'),
    path('print_receipt/<int:client_id>/<int:reservation_id>/', v.print_receipt, name='print_receipt'),
    path('fetch_rooms/', v.fetch_rooms, name='fetch_rooms'),
    path('search_reservation/', v.search_reservation, name='search_reservation'),
    path('reservation_details/<int:pk>/', v.reservation_details, name='reservation_details'),
    path('reservation/delete/<int:pk>/', v.delete_reservation, name='delete_reservation'),
    path('reservation_summary/<int:pk>/', v.reservation_summary, name='reservation_summary'),
    path('submit_reservation/', v.submit_reservation, name='submit_reservation'),
]
