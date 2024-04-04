from django.urls import path
from django.views.generic import TemplateView
from Reception import views as v

urlpatterns = [
    path("", v.receptionist_home, name="receptionist_home"),
    path('add-room-admin/', v.add_room_admin, name='add_room'),
    path('add-client-admin/', v.add_client_admin, name='add_client'),
    path('new-reservation-1/', v.new_reservation_1, name='new_reservation_1'),
    path('new-reservation-3/', v.new_reservation_3, name='new_reservation_3'),
    path('new-reservation-4/<int:pk>/', v.new_reservation_4, name='new_reservation_4'),
    path('check-in/', v.check_in_1, name='check_in'),
    path('check-in/summary/', v.check_in_summary, name='check_in_summary'),
    path('print-receipt/<int:client_id>/<int:reservation_id>/', v.print_receipt, name='print_receipt'),
    path('fetch-rooms/', v.fetch_rooms, name='fetch_rooms'),
    path('search-reservation/', v.search_reservation, name='search_reservation'),
    path('reservation-details/<int:pk>/', v.reservation_details, name='reservation_details'),
    path('reservation/delete/<int:pk>/', v.delete_reservation, name='delete_reservation'),
    path('submit-reservation/', v.submit_reservation, name='submit_reservation'),
    path('check-out/', v.check_out_1, name='check_out'),
    path('check-out-summary/<int:pk>', v.check_out_summary, name='check_out_summary'),
    path('check-out-3/<int:pk>', v.check_out_3, name='check_out_3'),
    path('print-receipt/<int:client_id>/<int:reservation_id>/', v.print_receipt_check_out,
         name='print_receipt_check_out'),
]
