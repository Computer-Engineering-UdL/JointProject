from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User, AbstractUser


class HotelUser(AbstractUser):
    dni = models.CharField(max_length=9)
    email = models.EmailField()
    phone_number = models.CharField(max_length=9)

    def __str__(self):
        return self.first_name


class Worker(HotelUser):
    schedule = models.CharField(max_length=100)
    type = models.CharField(max_length=100)


class Client(HotelUser):
    is_hosted = models.BooleanField()


class Room(models.Model):
    ROOM_TYPES = [
        ('No seleccionat', 'No seleccionat'),
        ('Individual', 'Individual'),
        ('Double', 'Double'),
        ('Suite', 'Suite'),
        ('Deluxe', 'Deluxe')
    ]
    # client = models.ForeignKey(Client, on_delete=models.CASCADE)
    is_clean = models.BooleanField()
    is_taken = models.BooleanField()
    room_num = models.IntegerField()
    room_price = models.IntegerField()
    room_type = models.CharField(
        max_length=15,
        choices=ROOM_TYPES,
        default='Double'
    )

    def __str__(self):
        return str(self.id)


class RoomReservation(models.Model):
    PENSION_TYPES = [
        ('Sense pensió', 'Sense pensió'),
        ('Esmorzar Buffet', 'Esmorzar Buffet'),
        ('Completa', 'Completa')
    ]
    # client = models.ForeignKey(Client, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, to_field='id')
    entry = models.DateField()
    exit = models.DateField()
    pension_type = models.CharField(
        max_length=15,
        choices=PENSION_TYPES,
        default='Sense pensió'
    )
    num_guests = models.IntegerField()

    class Meta:
        unique_together = ('room', 'entry', 'exit')

    def __str__(self):
        return self.room.room_num

