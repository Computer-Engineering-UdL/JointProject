from django import forms
from Restaurant.models import RestaurantReservation, ExternalRestaurantClient
from Reception.models import HotelUser, Client
from Restaurant.config import Config as rc
from Reception import utils as u
from datetime import date
from django.core.exceptions import ValidationError
from django.db.models import Sum


def get_available_guests_number():
    today = date.today()
    total_guests = RestaurantReservation.objects.filter(day=today).aggregate(Sum('num_guests'))['num_guests__sum'] or 0
    return rc.MAX_GUESTS_PER_DAY - total_guests


class NewRestaurantReservationForm(forms.ModelForm):
    day = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), initial=date.today, label='Dia')
    num_guests = forms.ChoiceField(choices=[(i, i) for i in range(1, get_available_guests_number() + 1)],
                                   label='Nombre de clients')
    service = forms.ChoiceField(choices=rc.get_restaurant_services(), label='Servei')

    class Meta:
        model = RestaurantReservation
        fields = ['day', 'num_guests', 'service']

    def clean(self):
        cleaned_data = super().clean()
        day = cleaned_data.get('day')
        num_guests = cleaned_data.get('num_guests')
        service = cleaned_data.get('service')

        if day < date.today():
            raise ValidationError("No es pot reservar per a un dia passat")
        if day.year > date.today().year + 1:
            raise ValidationError("No es poden fer reserves per a més d'un any")

        if int(num_guests) > get_available_guests_number():
            raise ValidationError(f"El nombre màxim de convidats per aquest dia ha estat superat.")

        return cleaned_data


def get_available_clients():
    today = date.today()

    active_hosted_clients = Client.objects.filter(is_hosted=True, is_active=True)
    service = RestaurantReservation.objects.filter(day=today).first().service

    clients_with_today_reservations = RestaurantReservation.objects.filter(
        day=today,
        client__isnull=False,
        is_active=True,
        service=service
    ).values_list('client', flat=True)

    available_clients = active_hosted_clients.exclude(id__in=clients_with_today_reservations)

    return available_clients


class AddInternalClientForm(forms.ModelForm):
    client = forms.ModelChoiceField(queryset=None, label='Client Intern')

    class Meta:
        model = RestaurantReservation
        fields = ['client']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].queryset = get_available_clients()

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

    class Meta:
        model = ExternalRestaurantClient
        fields = ['first_name', 'last_name', 'email', 'phone_number']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if HotelUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Aquest correu electrònic ja està registrat")
        return email

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if HotelUser.objects.filter(phone_number=phone).exists():
            raise forms.ValidationError("Aquest telèfon ja està registrat")
        return phone
