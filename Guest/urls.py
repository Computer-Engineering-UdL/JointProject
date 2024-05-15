from django.urls import path
from . import views as v

urlpatterns = [
    path('', v.guest_home, name='guest_home'),
    path('room-reservation/', v.guest_room_reservation_1, name='guest_room_reservation'),
]
