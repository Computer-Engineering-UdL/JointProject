from django.shortcuts import render, get_object_or_404, redirect

from Reception.forms import RoomReservationForm
from Reception.models import RoomReservation, create_despesa, Room, Client
from Guest.config import Config as c
from Guest import utils
from django.contrib import messages
from datetime import datetime

from Guest.forms import RestaurantReservationForm, SearchClientForm


def guest_home(request):
    return render(request, c.get_guest_home_path())


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
            return redirect(c.get_guest_home_path())
    else:
        form = RoomReservationForm()

    return render(request, c.get_guest_path(1), {'form': form})


def guest_restaurant_reservation_1(request):
    if request.method == 'POST':
        form = RestaurantReservationForm(request.POST)
        if form.is_valid():
            reservation_data = form.cleaned_data
            reservation_data['day'] = reservation_data['day'].strftime('%Y-%m-%d')
            request.session['reservation_data'] = reservation_data
            return redirect('guest_restaurant_reservation_2')
    else:
        form = RestaurantReservationForm()
    return render(request, c.get_guest_path(2), {'form': form})


def guest_restaurant_reservation_2(request):
    reservation_data = request.session.get('reservation_data')
    if not reservation_data:
        return redirect('guest_restaurant_reservation_1')

    if request.method == 'POST':
        form = SearchClientForm(request.POST)

        if form.is_valid():
            client_type = utils.get_client_type(form.cleaned_data['id_number'])
            if client_type == 'internal':
                client = Client.objects.get(id_number=form.cleaned_data['id_number'])
                reservation_data['client'] = client
                request.session['reservation_data'] = reservation_data
                return redirect('guest_restaurant_reservation_3')

    else:
        form = SearchClientForm()
    return render(request, c.get_guest_path(3), {'form': form})
