from datetime import date
from django import forms
from django.core.validators import RegexValidator
from django.db.models import Sum
from User import validators as uv
from Restaurant.config import Config as rc
from Restaurant.models import RestaurantReservation, ExternalRestaurantClient


def verify_restaurant_reservation(day, num_guests):
    if day < date.today():
        print(day, date.today())
        raise forms.ValidationError("No es pot reservar per a un dia passat")

    if day.year > date.today().year + 1:
        raise forms.ValidationError("No es poden fer reserves per a més d'un any")

    total_guests = (RestaurantReservation.objects.filter(day=day)
                    .aggregate(Sum('num_guests'))['num_guests__sum'] or 0)
    if total_guests + int(num_guests) > rc.MAX_GUESTS_PER_DAY:
        raise forms.ValidationError(
            f"El nombre màxim de convidats per aquest dia ha estat superat ({total_guests})")


def verify_external_client_form(email, phonenum, first_name, last_name):
    if ExternalRestaurantClient.objects.filter(email=email).exists():
        raise forms.ValidationError("Aquest correu electrònic ja està registrat")

    if ExternalRestaurantClient.objects.filter(phone_number=phonenum).exists():
        raise forms.ValidationError("Aquest telèfon ja està registrat")

    if not uv.is_valid_phone(phonenum):
        raise forms.ValidationError("El numero de telèfon no és vàlid")

    if not uv.is_valid_name(first_name):
        raise forms.ValidationError("El nom no és vàlid")

    if not uv.is_valid_name(last_name):
        raise forms.ValidationError("El cognom no és vàlid")

    if not uv.is_valid_email(email):
        raise forms.ValidationError("El correu electrònic no és vàlid")
