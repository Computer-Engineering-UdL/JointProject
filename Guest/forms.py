from django import forms

from Reception.models import RoomReservation, Client, Room, HotelUser, ExtraCosts
from Reception.config import Config as c
from Reception import forms_verify as fv


class RoomReservationForm(forms.ModelForm):
    entry = forms.DateField(input_formats=['%d/%m/%Y'])
    exit = forms.DateField(input_formats=['%d/%m/%Y'])
    pension_type = forms.ChoiceField(choices=c.get_pension_types)
    num_guests = forms.IntegerField()
    room_type = forms.ChoiceField(choices=c.get_room_types)

    def __init__(self, *args, **kwargs):
        super(RoomReservationForm, self).__init__(*args, **kwargs)
        self.fields['room'].choices = [(room.id, room.room_num) for room in Room.objects.all()]
        self.fields['entry'].widget.attrs['id'] = 'entrada'
        self.fields['exit'].widget.attrs['id'] = 'sortida'

    def clean_room(self):
        room_id = self.cleaned_data.get('room')
        try:
            room_id = int(room_id)
        except ValueError:
            raise forms.ValidationError("No hi han habitacions d'aquest tipus disponibles")
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            raise forms.ValidationError("L'habitació seleccionada no existeix")
        return room

    def clean_client(self):
        client_id = self.cleaned_data.get('client')
        try:
            client_id = int(client_id)
        except ValueError:
            raise forms.ValidationError("El client seleccionat no existeix")
        try:
            client = Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            raise forms.ValidationError("El client seleccionat no existeix")
        return client

    def clean(self):
        cleaned_data = super().clean()
        entry = cleaned_data.get('entry')
        exit = cleaned_data.get('exit')

        try:
            fv.verify_room_reservation_form(entry, exit, cleaned_data.get('num_guests'), cleaned_data.get('room_type'))
        except TypeError:
            self.add_error(None, "La data introduïda no és vàlida")

        return cleaned_data

    class Meta:
        model = RoomReservation
        fields = ['entry', 'exit', 'pension_type', 'num_guests', 'room_type']
