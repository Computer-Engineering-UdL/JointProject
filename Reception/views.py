from django.http import JsonResponse, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from Reception.forms import AddClientForm, RoomReservationForm, RoomForm, SearchReservationForm, AddExtraCostsForm
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
            form.save()
            return redirect('receptionist_home')
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
            room_reservation = get_object_or_404(RoomReservation, pk=room_rsv.id)
            create_despesa(room_rsv, room_reservation.pension_type, room.room_type)
            return redirect('new_reservation_4', room_rsv.id)
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
    messages.success(request, "Reserva completada amb èxit")
    return redirect('receptionist_home')


@worker_required('receptionist')
def check_in_1(request):
    form = SearchReservationForm(request.GET or None)
    filtered_reservations, status = u.get_filtered_reservations(form, is_active=True, check_in_active=False,
                                                                check_out_active=False)

    if not status:
        messages.error(request, "No s'ha trobat cap reserva")

    return render(request, c.get_check_in_path(1), {
        'form': form,
        'reservations': filtered_reservations
    })


@worker_required('receptionist')
def check_in_summary(request, pk):
    try:
        reservation = RoomReservation.objects.get(id=pk, is_active=True, check_in_active=False)
        client = reservation.client

        if request.method == 'POST':
            action = request.POST.get('action')

            if action == 'print_receipt':
                return redirect('print_receipt', reservation_id=reservation.id)
            elif action == 'check_in':
                check_in, created = CheckIn.objects.get_or_create(
                    num_reservation=str(reservation.id),
                    defaults={'id_number': client.id_number}
                )

                if created:
                    check_in.save()
                    reservation.check_in_active = True
                    reservation.save()

                messages.success(request, "Check-in completat amb èxit")
                return redirect('check_in')

        client = reservation.client
        return render(request, c.get_check_in_path(2), {
            'client': client,
            'reservation': reservation,
            'check_in': None
        })

    except RoomReservation.DoesNotExist:
        messages.error(request, "No s'ha trobat la reserva")
        return redirect('check_in')
    except HotelUser.DoesNotExist:
        messages.error(request, "No s'ha trobat el client")
        return redirect('check_in')


@worker_required('receptionist')
def print_receipt(request, reservation_id):
    reservation = RoomReservation.objects.get(id=reservation_id)
    client = reservation.client

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
    filtered_reservations, status = u.get_filtered_reservations(form, is_active=True)

    if not status:
        messages.error(request, "No s'ha trobat cap reserva")

    return render(request, c.get_manage_reservation_path(1), {'form': form, 'reservations': filtered_reservations})


@worker_required('receptionist')
def reservation_details(request, pk):
    try:
        reservation = RoomReservation.objects.get(pk=pk)
    except RoomReservation.DoesNotExist:
        messages.error(request, "No s'ha trobat la reserva")
        return redirect('search_reservation')

    return render(request, c.get_manage_reservation_path(2), {'reservation': reservation})


@worker_required('receptionist')
def add_extra_costs(request, pk):
    reservation = get_object_or_404(RoomReservation, pk=pk)
    room = get_object_or_404(Room, pk=reservation.room_id)
    extra_costs = ExtraCosts.objects.filter(room_reservation=reservation.id)

    if request.method == 'POST':
        form = AddExtraCostsForm(request.POST)
        if form.is_valid():
            extra_costs_type = form.cleaned_data.get('extra_costs_type')
            extra_costs_price = form.cleaned_data.get('extra_costs_price')
            new_extra_cost = ExtraCosts(
                room_reservation=reservation,
                extra_costs_type=extra_costs_type,
                extra_costs_price=extra_costs_price
            )
            new_extra_cost.save()
            messages.success(request, "S'han afegit els costos extra a la reserva amb èxit")
            return redirect('check_out_summary', pk=pk)
    else:
        form = AddExtraCostsForm()

    return render(request, c.get_check_out_path(5), {
        'form': form,
        'reservation': reservation,
        'room': room,
        'extra_costs': extra_costs
    })


@worker_required('receptionist')
def delete_reservation(request, pk):
    reservation = get_object_or_404(RoomReservation, pk=pk)
    if request.method == 'POST':
        reservation.is_active = False
        reservation.save()
        messages.success(request, "La reserva s'ha eliminat amb èxit")
        return redirect('search_reservation')

    return redirect('reservation_details', pk=pk)


@worker_required('receptionist')
def check_out_1(request):
    form = SearchReservationForm(request.GET or None)
    filtered_reservations, status = u.get_filtered_reservations(form, is_active=True, check_in_active=True,
                                                                check_out_active=False)

    if not status:
        messages.error(request, "No s'ha trobat cap reserva")

    return render(request, c.get_check_out_path(1), {'form': form, 'reservations': filtered_reservations})


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
    reservation.check_out_active = True
    reservation.is_active = False
    room.save()
    # Enviar dades a les autoritats
    # return redirect('check_out_5')
    messages.success(request, "Check-out completat amb èxit")
    return render(request, c.get_check_out_path(4), {'reservation': reservation, 'client': client})


@worker_required('receptionist')
def print_receipt_check_out(request, reservation_id, client_id):
    client = HotelUser.objects.get(id=client_id)
    reservation = RoomReservation.objects.get(id=reservation_id)
    despeses = Despeses.objects.get(room_reservation_id=reservation_id)
    extra_costs = ExtraCosts.objects.filter(room_reservation=reservation.id)

    buffer = u.create_receipt_check_out(reservation, client, despeses, extra_costs)

    return FileResponse(buffer, as_attachment=True, filename=c.RECEIPT_CHECKOUT_FILENAME)
