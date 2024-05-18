from django.db import models

from Reception.models import Room


class CleaningMaterial(models.Model):
    material_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='cleaning_materials/')

    def __str__(self):
        return self.material_name


class Stock(models.Model):
    material = models.ForeignKey(CleaningMaterial, on_delete=models.CASCADE)
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

    def __str__(self):
        return f"{self.room} - {self.date}"
