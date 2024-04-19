from django.db import models

class Cleaning_Material(models.Model):
    material_name = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='cleaning_materials/')

    def __str__(self):
        return self.material_name


class Stock(models.Model):
    material = models.ForeignKey(Cleaning_Material, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    is_available = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.material.material_name
