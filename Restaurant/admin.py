from django.contrib import admin

from Restaurant.models import RestaurantReservation, ExternalRestaurantClient

admin.site.register(RestaurantReservation)
admin.site.register(ExternalRestaurantClient)
