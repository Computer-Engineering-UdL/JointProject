from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from Reception.models import HotelUser


class RestaurantReservation(models.Model):
    day = models.DateField()
    client = models.ForeignKey(HotelUser, on_delete=models.CASCADE)
    num_guests = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)])
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('day', 'client')

    def __str__(self):
        return f'{self.client.username} - {self.day}'
