from django.urls import path
from . import views as v

urlpatterns = [
    path('room_reservation/', v.guest_room_reservation_1, name='guest_room_reservation'),
    # add more paths here
]
