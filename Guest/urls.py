from django.urls import path
from . import views as v

urlpatterns = [
    path('', v.guest_home, name='guest_home'),
    path('room-reservation/', v.guest_room_reservation_1, name='guest_room_reservation'),
    path('room-reservation-2/', v.guest_room_reservation_2, name='guest_room_reservation_2'),
    path('room-reservation-3/<int:pk>/', v.guest_room_reservation_summary, name='guest_room_reservation_summary'),
    path('restaurant-reservation-1/', v.guest_restaurant_reservation_1, name='guest_restaurant_reservation_1'),
    path('restaurant-reservation-2/', v.guest_restaurant_reservation_2, name='guest_restaurant_reservation_2'),
    path('restaurant-reservation-3/', v.guest_restaurant_reservation_3, name='guest_restaurant_reservation_3'),
    path('restaurant-reservation-4/', v.guest_restaurant_reservation_4, name='guest_restaurant_reservation_4'),

]
