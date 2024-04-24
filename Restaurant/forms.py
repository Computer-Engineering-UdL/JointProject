from django import forms
from Restaurant.models import RestaurantReservation
from Reception.models import HotelUser, Client
from datetime import date


class NewRestaurantReservationForm(forms.ModelForm):
    day = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), initial=date.today, label='Dia')
    num_guests = forms.ChoiceField(choices=[(i, i) for i in range(1, 7)], label='Nombre de clients')
    client = forms.ModelChoiceField(queryset=Client.objects.all())

    class Meta:
        model = RestaurantReservation
        fields = ['day', 'num_guests', 'client']

    def clean_day(self):
        day = self.cleaned_data.get('day')
        if day < date.today():
            raise forms.ValidationError("No es pot reservar per a un dia passat")
        return day
