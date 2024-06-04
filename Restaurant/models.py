from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from Reception.models import HotelUser
from Restaurant.config import Config as rc


class RestaurantReservation(models.Model):
    day = models.DateField()
    num_guests = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(rc.MAX_GUESTS_PER_RESERVATION)]
    )
    is_active = models.BooleanField(default=True)

    client = models.ForeignKey(
        HotelUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reservations'
    )
    external_client = models.ForeignKey(
        'ExternalRestaurantClient',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reservations'
    )

    service = models.CharField(max_length=15, choices=rc.get_restaurant_services(), default='None')
    client_arrived = models.BooleanField(default=False)

    def __str__(self):
        if self.client:
            return f'Reservation for {self.client.username} on {self.day}'
        elif self.external_client:
            return f'Reservation for {self.external_client.first_name} {self.external_client.last_name} on {self.day}'
        else:
            return 'Reservation with unspecified client'


class ExternalRestaurantClient(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=9)

    def clean(self):
        if self.phone_number is None and self.email is None:
            raise ValidationError("Cal com a mínim un telèfon o correu electrònic")
        return self

    def __str__(self):
        return self.first_name + ' ' + self.last_name
