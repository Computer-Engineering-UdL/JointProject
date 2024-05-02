from django import forms
from Restaurant.models import RestaurantReservation
from Reception.models import HotelUser, Client
from Restaurant.config import Config as rc
from Reception import utils as u
from datetime import date
from django.core.exceptions import ValidationError
from django.db.models import Sum
from Restaurant import forms_verify as fv


class NewRestaurantReservationForm(forms.ModelForm):
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
            fv.verify_restaurant_reservation(day, num_guests)
        except forms.ValidationError as e:
            self.add_error(None, e)

        return cleaned_data


def get_available_clients():
    today = date.today()

    active_hosted_clients = Client.objects.filter(is_hosted=True, is_active=True)

    clients_with_today_reservations = RestaurantReservation.objects.filter(
        day=today,
        client__isnull=False,
        is_active=True
    ).values_list('client', flat=True)

    available_clients = active_hosted_clients.exclude(id__in=clients_with_today_reservations)

    return available_clients


class AddInternalClientForm(forms.ModelForm):
    client = forms.ModelChoiceField(
        queryset=get_available_clients(),
        label='Client Intern')

    class Meta:
        model = RestaurantReservation
        fields = ['client']

    def clean_client(self):
        client = self.cleaned_data.get('client')
        if client is None:
            raise forms.ValidationError("Aquest client no existeix o no està allotjat")
        return client


class CreateExternalClientForm(forms.ModelForm):
    first_name = forms.CharField(label='Nom')
    last_name = forms.CharField(label='Cognoms')
    email = forms.EmailField(label='Correu electrònic')
    phone_number = forms.CharField(label='Telèfon')

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        phone_number = cleaned_data.get('phone_number')
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        try:
            fv.verify_external_client_form(email, phone_number, first_name, last_name)
        except ValidationError as e:
            self.add_error(None, e)

        return cleaned_data

    class Meta:
        model = HotelUser
        fields = ['first_name', 'last_name', 'email', 'phone_number']
