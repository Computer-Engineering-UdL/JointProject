from django.db import models

from Reception.models import Room


class Cleaning_Material(models.Model):
    material_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='cleaning_materials/')

    def __str__(self):
        return self.material_name


class Stock(models.Model):
    material = models.ForeignKey(Cleaning_Material, on_delete=models.CASCADE)
    price = models.FloatField()
    is_available = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.material.material_name


class CleanedRoom(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    missing_objects = models.TextField(blank=True)
    need_towels = models.IntegerField(default=0)
    additional_comments = models.TextField(blank=True)
    is_cleaned = models.BooleanField(default=False)

    def __str__(self):
        return self.room.room_num
