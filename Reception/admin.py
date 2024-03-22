from django.contrib import admin
from .models import Worker, Client, Room, RoomReservation, HotelUser

# Register your models here.

admin.site.register(Worker)
admin.site.register(Client)
admin.site.register(Room)
admin.site.register(RoomReservation)
admin.site.register(HotelUser)
