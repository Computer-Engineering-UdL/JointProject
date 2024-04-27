from django.core.exceptions import ValidationError
from django import forms
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from Reception.models import HotelUser


class RestaurantReservation(models.Model):
    day = models.DateField()
    num_guests = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)]
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
    phone = models.CharField(max_length=9)

    def clean(self):
        if self.phone is None and self.email is None:
            raise ValidationError("Cal com a mínim un telèfon o correu electrònic")
        return self

    def __str__(self):
        return self.first_name + ' ' + self.last_name
