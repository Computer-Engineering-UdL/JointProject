from django.contrib.auth.models import User, AbstractUser
from django.db import models

from Reception.config import Config as c


class HotelUser(AbstractUser):
    email = models.EmailField()
    phone_number = models.CharField(max_length=c.PHONE_NUMBER_LENGTH)
    id_number = models.CharField(max_length=c.ID_NUMBER, blank=True, unique=True)

    def __str__(self):
        return self.first_name


class Worker(HotelUser):
    type = models.CharField(max_length=c.TEXT_SIZE)

    def is_receptionist(self):
        return self.type.lower() == 'receptionist'

    def is_cleaner(self):
        return self.type.lower() == 'cleaner'

    def is_restaurant(self):
        return self.type.lower() == 'restaurant'

    def is_accountant(self):
        return self.type.lower() == 'accountant'

    def is_planner(self):
        return self.type.lower() == 'planner'

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.type}"


class Client(HotelUser):
    is_hosted = models.BooleanField()


class Room(models.Model):
    is_clean = models.BooleanField()
    is_taken = models.BooleanField()
    room_num = models.IntegerField(unique=True)
    room_type = models.CharField(
        max_length=c.DROPDOWN_MAX_LENGTH,
        choices=c.get_room_types,
        default='Double'
    )
    room_price = models.IntegerField(default=0)
    cleaner = models.ForeignKey(Worker, on_delete=models.SET_NULL, null=True, blank=True,
                                limit_choices_to={'type': 'cleaner'})

    def save(self, *args, **kwargs):
        if not self.pk and not self.room_price:
            self.room_price = c.get_room_prices_per_type(self.room_type)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Room {self.room_num} ({self.room_type})"


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
    tourist_tax_paid = models.BooleanField(default=False)

    class Meta:
        unique_together = ('room', 'entry', 'exit')

    def __str__(self):
        return f"Reservation {self.id} - for Room {self.room.room_num} ({self.room.room_type})"


def create_despesa(room_reservation, pension_type, room_type):
    pension_cost = c.get_pension_cost_per_type(pension_type)
    room_cost = c.get_room_prices_per_type(room_type)

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
