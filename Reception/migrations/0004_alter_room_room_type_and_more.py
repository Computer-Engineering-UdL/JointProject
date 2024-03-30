# Generated by Django 5.0.3 on 2024-03-26 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reception', '0003_alter_room_room_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='room_type',
            field=models.CharField(choices=[('No seleccionat', 'No seleccionat'), ('Individual', 'Individual'), ('Double', 'Double'), ('Suite', 'Suite'), ('Deluxe', 'Deluxe')], default='Double', max_length=15),
        ),
        migrations.AlterField(
            model_name='roomreservation',
            name='pension_type',
            field=models.CharField(choices=[('Sense pensió', 'Sense pensió'), ('Esmorzar Buffet', 'Esmorzar Buffet'), ('Completa', 'Completa')], default='Sense pensió', max_length=15),
        ),
    ]