import dateutil.utils
from django import forms
from User.validators import is_valid_id_number
from Reception.models import RoomReservation, Client, Room, CheckIn, HotelUser


def verify_search_reservation_form(num_reservation, id_number, room_num):
    if not any([num_reservation, id_number, room_num]):
        raise forms.ValidationError("Introdueix informació en algun dels camps per a la cerca")

    if num_reservation and not num_reservation.isdigit():
        raise forms.ValidationError("Introdueix un número de reserva vàlid")

    if id_number and not is_valid_id_number(id_number):
        raise forms.ValidationError("Introdueix un número d'identificació vàlid")

    # Room num is not required to be validated since it is an integer field

    if room_num and not Room.objects.filter(room_num=room_num).exists():
        raise forms.ValidationError("No existeix cap habitació amb aquest número")

    if room_num and not RoomReservation.objects.filter(room__room_num=room_num).exists():
        raise forms.ValidationError("No existeix cap reserva per aquesta habitació")

    if num_reservation and not RoomReservation.objects.filter(id=num_reservation).exists():
        raise forms.ValidationError("No existeix cap reserva amb aquest número")

    if id_number and not HotelUser.objects.filter(id_number=id_number).exists():
        raise forms.ValidationError("No existeix cap client amb aquest número d'identificació")


def verify_room_reservation_form(entry_date, exit_date, hosts_num, room_type):
    if entry_date > exit_date:
        raise forms.ValidationError("La data d'entrada no pot ser posterior a la data de sortida")

    if hosts_num < 1:
        raise forms.ValidationError("El nombre d'hostes ha de ser com a mínim 1")

    if hosts_num > 6:
        raise forms.ValidationError("El nombre d'hostes no pot ser superior a 6")

    if room_type == "Individual" and hosts_num != 1:
        raise forms.ValidationError("Les habitacions individuals només poden allotjar un hoste")

    if room_type == "Double" and hosts_num != 2:
        raise forms.ValidationError("Les habitacions dobles només poden allotjar dos hostes")

    if room_type == "No seleccionat":
        raise forms.ValidationError("Selecciona un tipus d'habitació")
