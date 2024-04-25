from django import forms
from Restaurant.models import RestaurantReservation
from Reception.models import HotelUser, Client
from Restaurant.config import Config as rc
from Reception import utils as u
from datetime import date
from django.core.exceptions import ValidationError
from django.db.models import Sum


class NewRestaurantReservationForm(forms.ModelForm):
    day = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), initial=date.today, label='Dia')
    num_guests = forms.ChoiceField(choices=[(i, i) for i in range(1, rc.MAX_GUESTS_PER_RESERVATION + 1)],
                                   label='Nombre de clients')

    class Meta:
        model = RestaurantReservation
        fields = ['day', 'num_guests']

    def clean(self):
        cleaned_data = super().clean()
        day = cleaned_data.get('day')
        num_guests = cleaned_data.get('num_guests')

        if day < date.today():
            raise ValidationError("No es pot reservar per a un dia passat")
        if day.year > date.today().year + 1:
            raise ValidationError("No es poden fer reserves per a més d'un any")

        total_guests = RestaurantReservation.objects.filter(day=day).aggregate(Sum('num_guests'))[
                           'num_guests__sum'] or 0
        if total_guests + int(num_guests) > rc.MAX_GUESTS_PER_DAY:
            raise ValidationError(
                f"El nombre màxim de convidats per aquest dia ha estat superat. Ja estan reservats {total_guests} convidats.")

        return cleaned_data


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
    client = forms.ModelChoiceField(queryset=u.get_external_clients(), label='Client Extern')

    class Meta:
        model = RestaurantReservation
        fields = ['client']

    def clean_client(self):
        client = self.cleaned_data.get('client')
        if client is None:
            raise forms.ValidationError("Aquest client no existeix")
        return client
