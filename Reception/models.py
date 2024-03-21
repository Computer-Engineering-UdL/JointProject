from django.db import models
from django.contrib.auth.models import User
from django.db.models import Model


# Create your models here.
class Worker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    schedule = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    def __str__(self):
        return self.user.first_name

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_hosted = models.BooleanField()
    def __str__(self):
        return self.user.first_name

class Room(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    is_clean = models.BooleanField()
    is_taken = models.BooleanField()
    room_num = models.IntegerField()
    room_price = models.IntegerField()

    def __str__(self):
        return self.room_num
class Room_reservation(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    pension_type = models.CharField(max_length=100)
    num_guests = models.IntegerField()

    class Meta:
        unique_together = ('room', 'check_in', 'check_out')
    def __str__(self):
        return self.room.room_num




