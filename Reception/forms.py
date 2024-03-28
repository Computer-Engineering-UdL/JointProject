from django import forms
from django.contrib.auth import get_user_model

from .models import RoomReservation, Client, Room


class RoomForm(forms.ModelForm):
    ROOM_TYPES = [
        ('Individual', 'Individual'),
        ('Double', 'Double'),
        ('Suite', 'Suite'),
        ('Deluxe', 'Deluxe')
    ]
    is_clean = forms.BooleanField(required=False)
    is_taken = forms.BooleanField(required=False)
    room_num = forms.IntegerField()
    room_price = forms.IntegerField()
    room_type = forms.ChoiceField(choices=ROOM_TYPES)

    class Meta:
        model = Room
        fields = ['room_num', 'room_price', 'room_type', 'is_clean', 'is_taken']


class RoomReservationForm(forms.ModelForm):
    PENSION_TYPES = [
        ('Esmorzar Buffet', 'Esmorzar Buffet'),
        ('Completa', 'Completa'),
        ('Sense pensió', 'Sense pensió')
    ]
    check_in = forms.DateField(input_formats=['%d/%m/%Y'])
    check_out = forms.DateField(input_formats=['%d/%m/%Y'])
    pension_type = forms.ChoiceField(choices=PENSION_TYPES)
    num_guests = forms.IntegerField()
    room = forms.ModelChoiceField(queryset=Room.objects.all())
    client = forms.ModelChoiceField(queryset=Client.objects.all())

    class Meta:
        model = RoomReservation
        fields = ['check_in', 'check_out', 'pension_type', 'num_guests', 'room', 'client']


class AddClientForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    dni = forms.CharField(max_length=9)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=9)
    is_hosted = forms.BooleanField(required=False)

    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'dni', 'email', 'phone_number', 'is_hosted']

#Check-in forms

class InfoClientForm(forms.ModelForm):

    num_reservation = forms.CharField(label="Introduce el número de reserva")
    dni = forms.CharField(max_length=9, label="Introduce el DNI")

    class Meta:
        model = RoomReservation
        fields = ['num_reservation', 'dni']






