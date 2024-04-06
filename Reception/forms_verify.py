from django import forms
from User.validators import is_valid_id_number
from Reception.models import RoomReservation, Client, Room, CheckIn, HotelUser


def verify_search_reservation_form(num_reservation, id_number, room_num):
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
