from django.contrib import admin
from .models import Worker, Client, Room, RoomReservation, HotelUser


admin.site.register(Worker)
admin.site.register(Client)
admin.site.register(Room)
admin.site.register(RoomReservation)
admin.site.register(HotelUser)
