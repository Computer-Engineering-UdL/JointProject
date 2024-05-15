from django.shortcuts import render, get_object_or_404, redirect

from Reception.forms import RoomReservationForm
from Reception.models import RoomReservation, create_despesa, Room, Client
from Reception.config import Config as c
from django.contrib import messages
from datetime import datetime


def guest_home(request):
    return render(request, c.get_guest_path(2))

def guest_room_reservation_1(request):
    """Client creates a new reservation."""
    if request.method == 'POST':
        form = RoomReservationForm(request.POST)
        """Get the first available room of the chosen type."""
        try:
            room = Room.objects.filter(room_type=request.POST.get('room_type'), is_taken=False).first()
        except Room.DoesNotExist:
            messages.error(request, "No hi han habitacions d'aquest tipus disponibles.")
            room = None

        """Get the client based on the current user session."""
        try:
            client = Client.objects.get(id=request.user.id)
        except Client.DoesNotExist:
            messages.error(request, "Error al rebre les dades del client. Torna-ho a intentar")
            client = None

        if room and client:
            entry_date = datetime.strptime(request.POST.get('entry'), '%d/%m/%Y').strftime('%Y-%m-%d')
            exit_date = datetime.strptime(request.POST.get('exit'), '%d/%m/%Y').strftime('%Y-%m-%d')
            new_rsv = RoomReservation(
                client=client,
                room=room,
                entry=entry_date,
                exit=exit_date,
                pension_type=request.POST.get('pension_type'),
                num_guests=request.POST.get('num_guests')
            )
            room.is_taken = True
            room.save()
            new_rsv.save()
            create_despesa(new_rsv, new_rsv.pension_type, room.room_type)
            return redirect(c.get_guest_path(1))
    else:
        form = RoomReservationForm()

    return render(request, c.get_guest_path(2), {'form': form})