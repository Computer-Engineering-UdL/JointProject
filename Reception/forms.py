from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

from Reception.models import RoomReservation, Client, Room, HotelUser, ExtraCosts
from Reception.config import Config as c
from Reception import forms_verify as fv


class RoomReservationForm(forms.ModelForm):
    entry = forms.DateField(input_formats=['%d/%m/%Y'])
    exit = forms.DateField(input_formats=['%d/%m/%Y'])
    pension_type = forms.ChoiceField(choices=c.get_pension_types)
    num_guests = forms.IntegerField()
    room_type = forms.ChoiceField(choices=c.get_room_types)
    room = forms.ChoiceField()
    client = forms.ModelChoiceField(queryset=Client.objects.all(), empty_label="Select a client")

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
            raise forms.ValidationError("L'habitació seleccionada no és vàlida")
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            raise forms.ValidationError("L'habitació seleccionada no existeix")
        return room

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
        fields = ['entry', 'exit', 'pension_type', 'num_guests', 'room_type', 'room', 'client']


class AddClientForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    id_number = forms.CharField(max_length=20)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=9)
    is_hosted = forms.BooleanField(required=False)

    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'id_number', 'email', 'phone_number', 'is_hosted']

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        id_number = cleaned_data.get('id_number')
        email = cleaned_data.get('email')
        phone_number = cleaned_data.get('phone_number')

        try:
            fv.verify_client_form(first_name, last_name, id_number, email, phone_number)
        except ValidationError as e:
            self.add_error(None, e)


class SearchReservationForm(forms.ModelForm):
    num_reservation = forms.CharField(label="Número de reserva", required=False)
    id_number = forms.CharField(label="Document identificatiu", required=False)
    room_num = forms.IntegerField(label="Número d'habitació", required=False,
                                  validators=[MinValueValidator(1)])

    def clean(self):
        cleaned_data = super().clean()
        num_reservation = cleaned_data.get("num_reservation")
        id_number = cleaned_data.get("id_number")
        room_num = cleaned_data.get("room_num")

        fv.verify_search_reservation_form(num_reservation, id_number, room_num)

        return cleaned_data

    class Meta:
        model = RoomReservation
        fields = ['num_reservation', 'id_number', 'room_num']


class AddExtraCostsForm(forms.ModelForm):
    extra_costs_price = forms.IntegerField(label="Preu dels costs addicionals", validators=[MinValueValidator(0)])
    extra_costs_type = forms.ChoiceField(label="Tipus de cost addicional", choices=c.get_room_extra_costs)

    class Meta:
        model = ExtraCosts
        fields = ['extra_costs_price', 'extra_costs_type']
