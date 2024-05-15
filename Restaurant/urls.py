from django.urls import path
from django.views.generic import TemplateView
from Restaurant import views as v

urlpatterns = [
    path("", v.restaurant_home, name="restaurant_home"),
    path("new-reservation-1/", v.new_restaurant_reservation_1, name="new_restaurant_reservation_1"),
    path("new-reservation-2/", v.new_restaurant_reservation_2, name="new_restaurant_reservation_2"),
    path("new-reservation-3/", v.new_restaurant_reservation_3, name="new_restaurant_reservation_3"),
    path("reservations/", v.restaurant_reservations, name="restaurant_reservations"),
    path("reservations/delete/<int:pk>/", v.delete_restaurant_reservation, name="delete_restaurant_reservation"),
    path("reservations/confirm/<int:pk>/", v.confirm_restaurant_reservation, name="confirm_restaurant_reservation"),
]
