from django.contrib import admin
from .models import Worker, Client, Room, Room_reservation

# Register your models here.

admin.site.register(Worker)
admin.site.register(Client)
admin.site.register(Room)
admin.site.register(Room_reservation)
