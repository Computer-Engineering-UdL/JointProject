from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from Reception.config import Config as c


class HotelUser(AbstractUser):
    email = models.EmailField()
    phone_number = models.CharField(max_length=9)
    id_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.first_name


class Worker(HotelUser):
    schedule = models.CharField(max_length=100)
    type = models.CharField(max_length=100)


class Client(HotelUser):
    is_hosted = models.BooleanField()


class Room(models.Model):
    is_clean = models.BooleanField()
    is_taken = models.BooleanField()
    room_num = models.IntegerField()
    room_price = models.IntegerField()
    room_type = models.CharField(
        max_length=15,
        choices=c.get_room_types,
        default='Double'
    )

    def __str__(self):
        return str(self.id)


class RoomReservation(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, to_field='id')
    entry = models.DateField()
    exit = models.DateField()
    pension_type = models.CharField(
        max_length=15,
        choices=c.get_pension_types,
        default='Sense pensió'
    )
    num_guests = models.IntegerField()

    class Meta:
        unique_together = ('room', 'entry', 'exit')

    def __str__(self):
        return self.room.room_num


class CheckIn(models.Model):
    num_reservation = models.CharField(max_length=5)
    id_number = models.CharField(max_length=20, db_default='12345678A')

    def __str__(self):
        return self.num_reservation


class Despeses(models.Model):
    room_reservation = models.OneToOneField(RoomReservation, on_delete=models.CASCADE)
    pension_costs = models.IntegerField()
    room_type_costs = models.IntegerField()


class ExtraCosts(models.Model):
    room_reservation = models.ForeignKey(RoomReservation, on_delete=models.CASCADE)
    extra_costs_type = models.CharField(max_length=100, choices=c.get_room_extra_costs)
    extra_costs_price = models.IntegerField()
