from django import forms
from User import validators as uv


def verify_search_reservation_form(id_number):
    if not id_number:
        raise forms.ValidationError("Introdueix el teu número d'identificació")

    if id_number and not uv.is_valid_id_number(id_number):
        raise forms.ValidationError("Introdueix un número d'identificació vàlid")
