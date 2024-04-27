# Generated by Django 5.0.3 on 2024-04-27 12:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Restaurant', '0003_restaurantreservation_external_client'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='restaurantreservation',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='restaurantreservation',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reservations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='restaurantreservation',
            name='external_client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reservations', to='Restaurant.externalrestaurantclient'),
        ),
    ]