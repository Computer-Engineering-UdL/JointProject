# Generated by Django 5.0.3 on 2024-05-06 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Restaurant', '0006_restaurantreservation_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurantreservation',
            name='client_arrived',
            field=models.BooleanField(default=False),
        ),
    ]