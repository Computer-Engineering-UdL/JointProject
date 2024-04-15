from django.http import JsonResponse, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from Reception.forms import AddClientForm, RoomReservationForm, RoomForm, InfoClientForm, SearchReservationForm
from Reception.models import Room, RoomReservation, Client, HotelUser, CheckIn, Despeses, ExtraCosts, create_despesa
from User.decorators import worker_required, admin_required
from Reception.config import Config as c
from Reception import utils as u


@worker_required('receptionist')
def receptionist_home(request):
    return render(request, 'worker/receptionist/receptionist_home.html')


@admin_required
def add_client_admin(request):
    """Add a new client to the database."""
    if request.method == 'POST':
        form = AddClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.username = f"{client.first_name}_{client.last_name}"
            client.save()
    else:
        form = AddClientForm()

    return render(request, c.get_admin_tests_path(1), {'form': form})


@admin_required
def add_room_admin(request):
    """Add a new room to the database."""
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            chosen_room = form.cleaned_data['room']
            Room.objects.get(id=chosen_room.id)
            form.save()
    else:
        form = RoomForm()

    return render(request, c.get_admin_tests_path(2), {'form': form})


@worker_required('receptionist')
def new_reservation_1(request):
    """Reserve a room for a client."""
    if request.method == 'POST':
        form = RoomReservationForm(request.POST)
        if form.is_valid():
            room_rsv = form.save(commit=False)
            room = get_object_or_404(Room, pk=room_rsv.room_id)
            room.is_taken = True
            room_rsv.save()
            room.save()
            create_despesa(room_rsv, 0, 0)
            return redirect('new_reservation_4', room_rsv.id)
        else:
            form.add_error(None, "Error en el formulari")
    else:
        form = RoomReservationForm()

    return render(request, c.get_reservation_path(1), {'form': form})


@worker_required('receptionist')
def new_reservation_3(request):
    """Add a new client to the database."""
    if request.method == 'POST':
        form = AddClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.username = f"{client.first_name}_{client.last_name}"
            client.save()

            return redirect('new_reservation_1')
    else:
        form = AddClientForm()

    return render(request, c.get_reservation_path(3), {'form': form})


@worker_required('receptionist')
def new_reservation_4(request, pk):
    try:
        reservation = RoomReservation.objects.get(pk=pk)
        client = HotelUser.objects.get(id=reservation.client_id)
    except RoomReservation.DoesNotExist:
        messages.error(request, "No s'ha trobat la reserva")
        return redirect('search_reservation')

    return render(request, c.get_reservation_path(4), {'reservation': reservation, 'client': client})


@worker_required('receptionist')
def submit_reservation(request):
    return redirect('receptionist_home')


"""
@worker_required('receptionist')
def check_in_1(request):
    # Process to filter the client and reservation for check-in.
    if request.method == 'POST':
        form = InfoClientForm(request.POST)
        if form.is_valid():
            num_reservation = form.cleaned_data['num_reservation']
            id_number = form.cleaned_data['id_number']
            client = None
            reservation = None

            if num_reservation:
                try:
                    reservation = RoomReservation.objects.get(id=num_reservation)
                    client_id = reservation.client_id
                    client = HotelUser.objects.get(id=client_id)

                except RoomReservation.DoesNotExist:
                    pass
            if id_number and not client:
                try:
                    client = HotelUser.objects.get(id_number=id_number)
                    reservation = RoomReservation.objects.get(client_id=client.id)

                except HotelUser.DoesNotExist:
                    pass
                except RoomReservation.DoesNotExist:
                    pass

            if client and reservation and not CheckIn.objects.filter(num_reservation=reservation.id).exists():
                check_in = CheckIn.objects.create(num_reservation=reservation.id, id_number=client.id)
                check_in.save()

                request.session['reservation_id'] = reservation.id
                request.session['client_id'] = client.id
                return render(request, c.get_check_in_path(2), {'client': client, 'reservation': reservation})
            else:
                if client is None or reservation is None:
                    form.add_error(None, "No existeix cap reserva amb aquestes dades")
                elif CheckIn.objects.filter(num_reservation=reservation.id).exists():
                    form.add_error(None, "Ja s'ha fet el check-in d'aquesta reserva")
    else:
        form = InfoClientForm()

    return render(request, c.get_check_in_path(1), {'form': form})
"""


@worker_required('receptionist')
def check_in_1(request):
    form = InfoClientForm(request.GET or None)
    reservations = RoomReservation.objects.filter(is_active=True, check_in_active=False, check_out_active=False)

    if form.is_valid():
        num_reservation = form.cleaned_data.get('num_reservation')
        id_number = form.cleaned_data.get('id_number')
        room_num = form.cleaned_data.get('room_num')

        if num_reservation:
            reservations = reservations.filter(id=num_reservation)
        if id_number:
            reservations = reservations.filter(client__id_number=id_number)
        if room_num:
            reservations = reservations.filter(room__room_num=room_num)

    return render(request, c.get_check_in_path(1), {'form': form, 'reservations': reservations})


@worker_required('receptionist')
def check_in_summary(request):
    reservation_id = request.session.get('reservation_id')
    client_id = request.session.get('client_id')

    if reservation_id and client_id:
        try:
            reservation = RoomReservation.objects.get(id=reservation_id, is_active=True)
            client = HotelUser.objects.get(id=client_id)
            check_in, created = CheckIn.objects.get_or_create(
                num_reservation=str(reservation_id),
                defaults={'id_number': client.id_number}
            )

            if created:
                check_in.save()

            return render(request, c.get_check_in_path(4),
                          {'client': client, 'reservation': reservation, 'check_in': check_in})
        except (RoomReservation.DoesNotExist, HotelUser.DoesNotExist):
            messages.error(request, "No s'ha trobat la reserva")
            return redirect('check_in')

    else:
        messages.error(request, "No s'ha trobat o la reserva o el client")
        return redirect('check_in')

"""
@worker_required('receptionist')
def check_in_summary(request):
    reservation_id = request.session.get('reservation_id')
    client_id = request.session.get('client_id')
    reservation = RoomReservation.objects.get(id=reservation_id)
    client = HotelUser.objects.get(id=client_id)

    return render(request, c.get_check_in_path(4), {'client': client, 'reservation': reservation})
"""

@worker_required('receptionist')
def print_receipt(request, client_id, reservation_id):
    client = HotelUser.objects.get(id=client_id)
    reservation = RoomReservation.objects.get(id=reservation_id)

    buffer = u.create_receipt_check_in(reservation, client)

    return FileResponse(buffer, as_attachment=True, filename=c.RECEIPT_CHECKIN_FILENAME)


@worker_required('receptionist')
def fetch_rooms(request):
    room_type = request.GET.get('room_type')
    rooms = Room.objects.filter(room_type=room_type, is_taken=False).order_by('room_num')
    data = {'rooms': list(rooms.values('id', 'room_num'))}

    return JsonResponse(data)


@worker_required('receptionist')
def check_in_2(request):
    return render(request, c.get_check_in_path(2), {})


@worker_required('receptionist')
def search_reservation(request):
    form = SearchReservationForm(request.GET or None)
    reservations = RoomReservation.objects.all()

    if form.is_valid():
        num_reservation = form.cleaned_data.get('num_reservation')
        id_number = form.cleaned_data.get('id_number')
        room_num = form.cleaned_data.get('room_num')

        if num_reservation:
            reservations = reservations.filter(id=num_reservation)
        if id_number:
            reservations = reservations.filter(client__id_number=id_number)
        if room_num:
            reservations = reservations.filter(room__room_num=room_num)

    return render(request, c.get_manage_reservation_path(1), {'form': form, 'reservations': reservations})


@worker_required('receptionist')
def reservation_details(request, pk):
    try:
        reservation = RoomReservation.objects.get(pk=pk)
    except RoomReservation.DoesNotExist:
        messages.error(request, "No s'ha trobat la reserva")
        return redirect('search_reservation')

    return render(request, c.get_manage_reservation_path(2), {'reservation': reservation})


@worker_required('receptionist')
def delete_reservation(request, pk):
    reservation = get_object_or_404(RoomReservation, pk=pk)
    if request.method == 'POST':
        reservation.delete()
        messages.success(request, "La reserva s'ha eliminat amb èxit")
        return redirect('search_reservation')

    return redirect('reservation_details', pk=pk)


@worker_required('receptionist')
def check_out_1(request):
    form = SearchReservationForm(request.GET or None)
    reservations = RoomReservation.objects.all()

    if form.is_valid():
        num_reservation = form.cleaned_data.get('num_reservation')
        id_number = form.cleaned_data.get('id_number')
        room_num = form.cleaned_data.get('room_num')

        reservations = RoomReservation.objects.all()

        if num_reservation:
            reservations = reservations.filter(id=num_reservation, room__is_taken=True)
        if id_number:
            reservations = reservations.filter(client__id_number=id_number, room__is_taken=True)
        if room_num:
            reservations = reservations.filter(room__room_num=room_num, room__is_taken=True)

    return render(request, c.get_check_out_path(1), {'form': form, 'reservations': reservations})


@worker_required('receptionist')
def check_out_summary(request, pk):
    """ Check-out step 2 """
    reservation = get_object_or_404(RoomReservation, pk=pk)
    room = get_object_or_404(Room, pk=reservation.room_id)
    despeses = get_object_or_404(Despeses, room_reservation_id=pk)
    extra_costs = ExtraCosts.objects.filter(room_reservation=reservation.id)

    extra_total = 0
    for extra in extra_costs:
        extra_total += extra.extra_costs_price

    total_price = despeses.pension_costs + despeses.room_type_costs + extra_total

    return render(request, c.get_check_out_path(2),
                  {'extra_costs': extra_costs, 'reservation': reservation, 'room': room, 'despeses': despeses,
                   'total_price': total_price, 'extra_total': extra_total})


@worker_required('receptionist')
def check_out_3(request, pk):
    """ Check-out step 3 """
    reservation = get_object_or_404(RoomReservation, pk=pk)
    room = get_object_or_404(Room, pk=reservation.room_id)
    client = get_object_or_404(HotelUser, id=reservation.client_id)
    room.is_clean = False
    room.is_taken = False
    room.save()
    # Enviar dades a les autoritats
    # return redirect('check_out_5')

    return render(request, c.get_check_out_path(3), {'reservation': reservation, 'client': client})


@worker_required('receptionist')
def print_receipt_check_out(request, reservation_id, client_id):
    client = HotelUser.objects.get(id=client_id)
    reservation = RoomReservation.objects.get(id=reservation_id)
    despeses = Despeses.objects.get(room_reservation_id=reservation_id)
    extra_costs = ExtraCosts.objects.filter(room_reservation=reservation.id)

    buffer = u.create_receipt_check_out(reservation, client, despeses, extra_costs)

    return FileResponse(buffer, as_attachment=True, filename=c.RECEIPT_CHECKOUT_FILENAME)
