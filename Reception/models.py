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
    room_type = models.CharField(
        max_length=c.DROPDOWN_MAX_LENGTH,
        choices=c.get_room_types,
        default='Double'
    )
    room_price = models.IntegerField(choices=c.get_room_prices_per_type,
                                     default=100)

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
    is_active = models.BooleanField(default=True)
    check_in_active = models.BooleanField(default=False)
    check_out_active = models.BooleanField(default=False)

    class Meta:
        unique_together = ('room', 'entry', 'exit')

    def __str__(self):
        return self.room.room_num


class CheckIn(models.Model):
    num_reservation = models.CharField(max_length=c.TEXT_SIZE)
    id_number = models.CharField(max_length=c.ID_NUMBER, db_default='12345678A')

    def __str__(self):
        return self.num_reservation


def create_despesa(room_reservation, pension_type, room_type):
    pension_cost = next((cost for name, cost in c.get_pension_cost_per_type() if name == pension_type), 0)
    room_cost = next((cost for name, cost in c.get_room_prices_per_type() if name == room_type), 0)

    despesa = Despeses(room_reservation=room_reservation, pension_costs=pension_cost, room_type_costs=room_cost)
    despesa.save()


class Despeses(models.Model):
    room_reservation = models.OneToOneField(RoomReservation, on_delete=models.CASCADE)
    pension_costs = models.IntegerField(default=0)
    room_type_costs = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.room_type_costs:
            self.room_type_costs = self.room_reservation.room.room_price
        super().save(*args, **kwargs)


class ExtraCosts(models.Model):
    room_reservation = models.ForeignKey(RoomReservation, on_delete=models.CASCADE)
    extra_costs_type = models.CharField(max_length=c.TEXT_SIZE, choices=c.get_room_extra_costs)
    extra_costs_price = models.IntegerField()
