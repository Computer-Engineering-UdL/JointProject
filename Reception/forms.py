from django import forms
from .models import RoomReservation


class RoomReservationForm(forms.ModelForm):
    class Meta:
        model = RoomReservation
        fields = ['Client: ', 'Data entrada:', 'Data sortida:', 'Tipus de pensió:', 'Nombre hostes']


class AddClientForm(forms.ModelForm):
    class Meta:
        model = RoomReservation
        fields = ['Nom:', 'Cognom:', 'DNI:', 'Data de naixement:', 'Telèfon:', 'Correu electrònic:', 'Està hospedat: ']
