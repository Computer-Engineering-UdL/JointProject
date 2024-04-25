from django import forms
from Restaurant.models import RestaurantReservation
from Reception.models import HotelUser, Client
from Restaurant.config import Config as rc
from datetime import date


class NewRestaurantReservationForm(forms.ModelForm):
    day = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), initial=date.today, label='Dia')
    num_guests = forms.ChoiceField(choices=[(i, i) for i in range(1, rc.MAX_GUESTS_PER_RESERVATION)],
                                   label='Nombre de clients')

    class Meta:
        model = RestaurantReservation
        fields = ['day', 'num_guests']

    def clean_day(self):
        day = self.cleaned_data.get('day')
        if day < date.today():
            raise forms.ValidationError("No es pot reservar per a un dia passat")
        if day.year > date.today().year + 1:
            raise forms.ValidationError("No es poden fer reserves per a més d'un any")
        return day


class AddInternalClientForm(forms.ModelForm):
    client = forms.ModelChoiceField(queryset=Client.objects.filter(is_hosted=True), label='Client Intern')

    class Meta:
        model = RestaurantReservation
        fields = ['client']

    def clean_client(self):
        client = self.cleaned_data.get('client')
        if client is None:
            raise forms.ValidationError("Aquest client no existeix o no està allotjat")
        return client


class AddExternalClientForm(forms.ModelForm):
    client = forms.ModelChoiceField(queryset=HotelUser.objects.filter(is_active=True), label='Client Extern')

    class Meta:
        model = RestaurantReservation
        fields = ['client']

    def clean_client(self):
        client = self.cleaned_data.get('client')
        if client is None:
            raise forms.ValidationError("Aquest client no existeix")
        return client
