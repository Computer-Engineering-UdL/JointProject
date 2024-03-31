# Generated by Django 5.0.3 on 2024-03-31 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reception', '0008_roomreservation_client'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hoteluser',
            name='is_staff',
            field=models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status'),
        ),
    ]