from django.db import models
from django.contrib.auth.models import User, AbstractUser
from Reception.config import Config as c


class HotelUser(AbstractUser):
    email = models.EmailField()
    phone_number = models.CharField(max_length=c.PHONE_NUMBER_LENGTH)
    id_number = models.CharField(max_length=c.ID_NUMBER, blank=True)

    def __str__(self):
        return self.first_name


class Worker(HotelUser):
    schedule = models.CharField(max_length=c.TEXT_SIZE)
    type = models.CharField(max_length=c.TEXT_SIZE)


class Client(HotelUser):
    is_hosted = models.BooleanField()


class Room(models.Model):
    is_clean = models.BooleanField()
    is_taken = models.BooleanField()
    room_num = models.IntegerField()
    room_price = models.IntegerField()
    room_type = models.CharField(
        max_length=c.DROPDOWN_MAX_LENGTH,
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
        max_length=c.DROPDOWN_MAX_LENGTH,
        choices=c.get_pension_types,
        default='Sense pensió'
    )
    num_guests = models.IntegerField()

    class Meta:
        unique_together = ('room', 'entry', 'exit')

    def __str__(self):
        return self.room.room_num


class CheckIn(models.Model):
    num_reservation = models.CharField(max_length=c.TEXT_SIZE)
    id_number = models.CharField(max_length=c.ID_NUMBER, db_default='12345678A')

    def __str__(self):
        return self.num_reservation


def create_despesa(room_reservation, pension_costs, room_type_costs):
    despesa = Despeses(room_reservation=room_reservation, pension_costs=pension_costs, room_type_costs=room_type_costs)
    despesa.save()


class Despeses(models.Model):
    room_reservation = models.OneToOneField(RoomReservation, on_delete=models.CASCADE)
    pension_costs = models.IntegerField(default=0)
    room_type_costs = models.IntegerField(default=0)


class ExtraCosts(models.Model):
    room_reservation = models.ForeignKey(RoomReservation, on_delete=models.CASCADE)
    extra_costs_type = models.CharField(max_length=c.TEXT_SIZE, choices=c.get_room_extra_costs)
    extra_costs_price = models.IntegerField()
