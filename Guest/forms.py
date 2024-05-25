from django import forms

from Reception.models import RoomReservation, Room, HotelUser
from Reception.config import Config as c
from Reception import forms_verify as fv
from Restaurant import forms_verify as rfv
from Restaurant.config import Config as rc
from Restaurant.models import RestaurantReservation
from Guest import forms_verify as gfv
from datetime import date


class GuestRoomReservationFormStep1(forms.ModelForm):
    entry = forms.DateField(input_formats=['%d/%m/%Y'])
    exit = forms.DateField(input_formats=['%d/%m/%Y'])
    room_type = forms.ChoiceField(choices=c.get_room_types)

    def __init__(self, *args, **kwargs):
        super(GuestRoomReservationFormStep1, self).__init__(*args, **kwargs)
        self.fields['entry'].widget.attrs['id'] = 'entrada'
        self.fields['exit'].widget.attrs['id'] = 'sortida'

    def clean(self):
        cleaned_data = super().clean()
        entry = cleaned_data.get('entry')
        exit = cleaned_data.get('exit')

        return cleaned_data

    class Meta:
        model = RoomReservation
        fields = ['entry', 'exit']

class GuestRoomReservationFormStep2(forms.ModelForm):
    pension_type = forms.ChoiceField(choices=c.get_pension_types)
    num_guests = forms.IntegerField()

    class Meta:
        model = RoomReservation
        fields = ['pension_type', 'num_guests']


class RestaurantReservationForm(forms.ModelForm):
    day = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), initial=date.today, label='Dia')
    num_guests = forms.ChoiceField(choices=[(i, i) for i in range(1, rc.MAX_GUESTS_PER_RESERVATION + 1)],
                                   label='Nombre de clients')
    service = forms.ChoiceField(choices=rc.get_restaurant_services(), label='Servei')

    class Meta:
        model = RestaurantReservation
        fields = ['day', 'num_guests']

    def clean(self):
        cleaned_data = super().clean()
        day = cleaned_data.get('day')
        num_guests = cleaned_data.get('num_guests')

        try:
            rfv.verify_restaurant_reservation(day, num_guests)
        except TypeError:
            self.add_error(None, "La data introduïda no és vàlida")
        except forms.ValidationError as e:
            self.add_error(None, e)

        return cleaned_data


class SearchClientForm(forms.Form):
    id_number = forms.CharField(label="Document identificatiu", required=True)

    def clean(self):
        cleaned_data = super().clean()
        id_number = cleaned_data.get("id_number")
        gfv.verify_search_reservation_form(id_number)
        return cleaned_data
