from io import BytesIO
from django.http import JsonResponse, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from reportlab.pdfgen import canvas
from Reception.forms import AddClientForm, RoomReservationForm, RoomForm, InfoClientForm, SearchReservationForm
from Reception.models import Room, RoomReservation, Client, HotelUser, CheckIn, Despeses, ExtraCosts
from User.decorators import worker_required, admin_required
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


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
    return render(request, 'admin-tests/add_client.html', {'form': form})


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
    return render(request, 'admin-tests/add_room.html', {'form': form})


# New reservation views

NEW_RESERVATION_1_PATH = 'worker/receptionist/reservation/new_reservation/new_reservation_1.html'
NEW_RESERVATION_2_PATH = 'worker/receptionist/reservation/new_reservation/new_reservation_2.html'
NEW_RESERVATION_3_PATH = 'worker/receptionist/reservation/new_reservation/new_reservation_3.html'
NEW_RESERVATION_4_PATH = 'worker/receptionist/reservation/new_reservation/new_reservation_4.html'


@worker_required('receptionist')
def new_reservation_1(request):
    """Reserve a room for a client."""
    if request.method == 'POST':
        form = RoomReservationForm(request.POST)
        if form.is_valid():
            room_rsv = form.save(commit=False)
            room_rsv.save()
            return redirect('new_reservation_4', room_rsv.id)
        else:
            form.add_error(None, "Error en el formulari")
    else:
        form = RoomReservationForm()
    return render(request, NEW_RESERVATION_1_PATH, {'form': form})


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
    return render(request, NEW_RESERVATION_3_PATH, {'form': form})


@worker_required('receptionist')
def new_reservation_4(request, pk):
    try:
        reservation = RoomReservation.objects.get(pk=pk)
    except RoomReservation.DoesNotExist:
        messages.error(request, "No s'ha trobat la reserva.")
        return redirect('search_reservation')

    return render(request, NEW_RESERVATION_4_PATH, {'reservation': reservation})


@worker_required('receptionist')
def submit_reservation(request):
    return redirect('receptionist_home')


# Check-in views

CHECK_IN_1_PATH = 'worker/receptionist/check-in/check_in_1.html'
CHECK_IN_2_PATH = 'worker/receptionist/check-in/check_in_2.html'
CHECK_IN_4_PATH = 'worker/receptionist/check-in/check_in_4.html'


@worker_required('receptionist')
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
                return render(request, CHECK_IN_2_PATH,
                              {'client': client, 'reservation': reservation})
            else:

                if client is None or reservation is None:
                    form.add_error(None, "No existeix cap reserva amb aquestes dades.")
                elif CheckIn.objects.filter(num_reservation=reservation.id).exists():
                    form.add_error(None, "Ja s'ha fet el check-in d'aquesta reserva.")

    else:
        form = InfoClientForm()
    return render(request, CHECK_IN_1_PATH, {'form': form})


@worker_required('receptionist')
def check_in_summary(request):
    reservation_id = request.session.get('reservation_id')
    client_id = request.session.get('client_id')
    reservation = RoomReservation.objects.get(id=reservation_id)
    client = HotelUser.objects.get(id=client_id)

    return render(request, CHECK_IN_4_PATH, {'client': client, 'reservation': reservation})


@worker_required('receptionist')
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


@worker_required('receptionist')
def fetch_rooms(request):
    room_type = request.GET.get('room_type')
    rooms = Room.objects.filter(room_type=room_type, is_taken=False).order_by('room_num')
    data = {'rooms': list(rooms.values('id', 'room_num'))}
    return JsonResponse(data)


@worker_required('receptionist')
def check_in_2(request):
    return render(request, CHECK_IN_2_PATH, {})


# Cancel reservation views

SEARCH_RESERVATION_PATH = 'worker/receptionist/reservation/manage_reservation/search_reservation.html'
RESERVATION_DETAIL_PATH = 'worker/receptionist/reservation/manage_reservation/reservation_details.html'


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

    return render(request, SEARCH_RESERVATION_PATH, {'form': form, 'reservations': reservations})


@worker_required('receptionist')
def reservation_details(request, pk):
    try:
        reservation = RoomReservation.objects.get(pk=pk)
    except RoomReservation.DoesNotExist:
        messages.error(request, "No s'ha trobat la reserva.")
        return redirect('search_reservation')

    return render(request, RESERVATION_DETAIL_PATH, {'reservation': reservation})


@worker_required('receptionist')
def delete_reservation(request, pk):
    reservation = get_object_or_404(RoomReservation, pk=pk)
    if request.method == 'POST':
        reservation.delete()
        messages.success(request, "La reserva s'ha eliminat amb èxit")
        return redirect('search_reservation')
    return redirect('reservation_details', pk=pk)


# Check-out views
CHECK_OUT_1_PATH = 'worker/receptionist/check-out/check_out_1.html'
CHECK_OUT_2_PATH = 'worker/receptionist/check-out/check_out_2.html'
CHECK_OUT_3_PATH = 'worker/receptionist/check-out/check_out_3.html'
CHECK_OUT_4_PATH = 'worker/receptionist/check-out/check_out_4.html'


@worker_required('receptionist')
def check_out_1(request):
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

    return render(request, CHECK_OUT_1_PATH, {'form': form, 'reservations': reservations})


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
    return render(request, CHECK_OUT_2_PATH,
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
    return render(request, CHECK_OUT_4_PATH, {'reservation': reservation, 'client': client})


@worker_required('receptionist')
def print_receipt_check_out(request, reservation_id, client_id):
    client = HotelUser.objects.get(id=client_id)
    reservation = RoomReservation.objects.get(id=reservation_id)
    despeses = Despeses.objects.get(room_reservation_id=reservation_id)
    extra_costs = ExtraCosts.objects.filter(room_reservation=reservation.id)

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    Story = []
    styles = getSampleStyleSheet()

    Story.append(Paragraph("Comprovant de Check-Out", styles['Title']))

    # Informació de la reserva
    Story.append(Paragraph(f"Número de reserva: {reservation.id}", styles['Normal']))
    Story.append(Paragraph(f"Data d'entrada: {reservation.entry}", styles['Normal']))
    Story.append(Paragraph(f"Data de sortida: {reservation.exit}", styles['Normal']))
    Story.append(Paragraph(f"Número d'hostes: {reservation.num_guests}", styles['Normal']))
    Story.append(Paragraph(f"Tipus de pensió: {reservation.pension_type}", styles['Normal']))
    Story.append(Paragraph(f"Tipus d'habitació: {reservation.room.room_type}", styles['Normal']))
    Story.append(Paragraph(f"Número d'habitació: {reservation.room.room_num}", styles['Normal']))
    Story.append(Spacer(1, 12))

    # Informació de despeses
    Story.append(Paragraph(f"Costs de pensió: {despeses.pension_costs}", styles['Normal']))
    Story.append(Paragraph(f"Costs de tipus d'habitació: {despeses.room_type_costs}", styles['Normal']))
    Story.append(Spacer(1, 12))

    # Informació de costos extra
    for extra in extra_costs:
        Story.append(Paragraph(f"Tipus de cost extra: {extra.extra_costs_type}", styles['Normal']))
        Story.append(Paragraph(f"Preu del cost extra: {extra.extra_costs_price}", styles['Normal']))
    Story.append(Spacer(1, 12))

    # Informació del client
    Story.append(Paragraph(f"Nom del client: {client.first_name} {client.last_name}", styles['Normal']))
    Story.append(Paragraph(f"Document d'identitat: {client.id_number}", styles['Normal']))
    Story.append(Paragraph(f"Correu electrònic: {client.email}", styles['Normal']))
    Story.append(Paragraph(f"Telèfon: {client.phone_number}", styles['Normal']))
    Story.append(Spacer(1, 12))

    # Final del document
    Story.append(Paragraph("Gràcies per la seva estada!", styles['Normal']))

    doc.build(Story)
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename='receipt.pdf')
