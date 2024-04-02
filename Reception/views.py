from io import BytesIO
from django.http import JsonResponse, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from reportlab.pdfgen import canvas
from Reception.forms import AddClientForm, RoomReservationForm, RoomForm, InfoClientForm, SearchReservationForm
from Reception.models import Room, RoomReservation, Client, HotelUser, CheckIn


@login_required
def worker_home(request):
    return render(request, 'worker/base_worker.html')


@login_required
def add_client_admin(request):
    """Add a new client to the database."""
    if request.method == 'POST':
        form = AddClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.username = 'default'
            client.save()
    else:
        form = AddClientForm()
    return render(request, 'admin-tests/add_client.html', {'form': form})


@login_required
def room_reservation(request):
    """Reserve a room for a client."""
    if request.method == 'POST':
        form = RoomReservationForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print("Form is not valid. Errors: ", form.errors)
    else:
        form = RoomReservationForm()
    return render(request, 'worker/receptionist/reservation/new_reservation/new_reservation_1.html', {'form': form})


@login_required
def add_room(request):
    """Add a new room to the database."""
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            chosen_room = form.cleaned_data['room']
            Room.objects.get(id=chosen_room.id)
            form.save()
    else:
        form = RoomForm()
    return render(request, 'worker/receptionist/reservation/new_reservation/new_reservation_2.html', {'form': form})


@login_required
def add_client(request):
    """Add a new client to the database."""
    if request.method == 'POST':
        form = AddClientForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = AddClientForm()
    return render(request, 'worker/receptionist/reservation/new_reservation/new_reservation_3.html', {'form': form})


# Check-in views
@login_required
def check_in_1(request):
    """Check-in a client."""
    if request.method == 'POST':
        form = InfoClientForm(request.POST)
        if form.is_valid():
            num_reservation = form.cleaned_data['num_reservation']
            dni = form.cleaned_data['dni']
            client = None
            reservation = None

            if num_reservation:
                try:
                    reservation = RoomReservation.objects.get(id=num_reservation)
                    client_id = reservation.client_id
                    client = HotelUser.objects.get(id=client_id)

                except RoomReservation.DoesNotExist:
                    pass
            if dni and not client:
                try:
                    client = HotelUser.objects.get(id_number=dni)
                    reservation = RoomReservation.objects.get(client_id=client.id)

                except HotelUser.DoesNotExist:
                    pass
                except RoomReservation.DoesNotExist:
                    pass

            if client and reservation and not CheckIn.objects.filter(num_reservation=reservation.id).exists():
                check_in = CheckIn.objects.create(num_reservation=reservation.id, dni=client.id)
                check_in.save()

                request.session['reservation_id'] = reservation.id
                request.session['client_id'] = client.id
                return render(request, 'worker/receptionist/check-in/check_in_2.html',
                              {'client': client, 'reservation': reservation})
            else:

                if client is None or reservation is None:
                    form.add_error(None, "No existeix cap reserva amb aquestes dades.")
                elif CheckIn.objects.filter(num_reservation=reservation.id).exists():
                    form.add_error(None, "Ja s'ha fet el check-in d'aquesta reserva.")

    else:
        form = InfoClientForm()
    return render(request, 'worker/receptionist/check-in/check_in_1.html', {'form': form})


def check_in_summary(request):
    reservation_id = request.session.get('reservation_id')
    client_id = request.session.get('client_id')
    reservation = RoomReservation.objects.get(id=reservation_id)
    client = HotelUser.objects.get(id=client_id)

    return render(request, 'worker/receptionist/check-in/check_in_4.html',
                  {'client': client, 'reservation': reservation})


def print_receipt(request, client_id, reservation_id):
    client = HotelUser.objects.get(id=client_id)
    reservation = RoomReservation.objects.get(id=reservation_id)

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)

    pdf.drawString(100, 750, "Comprovant de reserva")
    pdf.drawString(100, 735, f"Número de reserva: {reservation.id}")
    pdf.drawString(100, 720, f"Data de entrada: {reservation.entry}")
    pdf.drawString(100, 705, f"Data de sortida: {reservation.exit}")
    pdf.drawString(100, 690, f"Número de hostes: {reservation.num_guests}")
    pdf.drawString(100, 675, f"Tipus de pensió: {reservation.pension_type}")
    pdf.drawString(100, 660, f"Tipus de habitació: {reservation.room.room_type}")
    pdf.drawString(100, 645, f"Número de habitació: {reservation.room.room_num}")

    pdf.drawString(100, 630, f"Nom del client: {client.first_name} {client.last_name}")
    pdf.drawString(100, 615, f"Document identificatiu: {client.id_number}")
    pdf.drawString(100, 600, f"Email: {client.email}")
    pdf.drawString(100, 585, f"Telèfon: {client.phone_number}")

    pdf.showPage()
    pdf.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename='receipt.pdf')


@login_required
def fetch_rooms(request):
    room_type = request.GET.get('room_type')
    rooms = Room.objects.filter(room_type=room_type, is_taken=False).order_by('room_num')
    data = {'rooms': list(rooms.values('id', 'room_num'))}
    return JsonResponse(data)


@login_required
def check_in_2(request):
    return render(request, 'worker/receptionist/check-in/check_in_2.html', {})


# Cancel reservation views

SEARCH_RESERVATION_PATH = 'worker/receptionist/reservation/modify_reservation/search_reservation.html'
RESERVATION_DETAIL_PATH = 'worker/receptionist/reservation/modify_reservation/reservation_details.html'


@login_required
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

    return render(request, SEARCH_RESERVATION_PATH, {'form': form, 'reservations': reservations})


@login_required
def reservation_details(request, pk):
    try:
        reservation = RoomReservation.objects.get(pk=pk)
    except RoomReservation.DoesNotExist:
        messages.error(request, "No s'ha trobat la reserva.")
        return redirect('search_reservation')

    return render(request, RESERVATION_DETAIL_PATH, {'reservation': reservation})


@login_required
def delete_reservation(request, pk):
    reservation = get_object_or_404(RoomReservation, pk=pk)
    if request.method == 'POST':
        reservation.delete()
        messages.success(request, "La reserva s'ha eliminat amb èxit")
        return redirect('search_reservation')
    return redirect('reservation_details', pk=pk)
