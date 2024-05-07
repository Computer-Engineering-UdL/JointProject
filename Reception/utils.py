from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from Reception.models import HotelUser, Client, RoomReservation
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle


def get_external_clients():
    active_users = HotelUser.objects.filter(is_active=True)
    internal_clients_ids = Client.objects.all().values_list('id', flat=True)
    return active_users.exclude(id__in=internal_clients_ids)


def get_filtered_reservations(form, is_active=True, check_in_active=None, check_out_active=None) -> tuple:
    if check_in_active is None and check_out_active is None:
        reservations = RoomReservation.objects.filter(is_active=is_active)
    else:
        reservations = RoomReservation.objects.filter(is_active=is_active,
                                                      check_in_active=check_in_active,
                                                      check_out_active=check_out_active
                                                      )
    filtered_reservations = reservations

    if form.is_valid():
        num_reservation = form.cleaned_data.get('num_reservation')
        id_number = form.cleaned_data.get('id_number')
        room_num = form.cleaned_data.get('room_num')

        if num_reservation:
            filtered_reservations = filtered_reservations.filter(id=num_reservation)
        if id_number:
            filtered_reservations = filtered_reservations.filter(client__id_number=id_number)
        if room_num:
            filtered_reservations = filtered_reservations.filter(room__room_num=room_num)

        if not filtered_reservations.exists():
            return reservations, False

    return filtered_reservations, True


def create_receipt_check_in(reservation, client):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    styles = getSampleStyleSheet()

    # Capçalera
    header_data = [[Paragraph('Comprovant de Check-In', styles['Title'])]]
    header_table = Table(header_data, colWidths=[460])
    header_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))

    reservation_data = [
        [Paragraph('Informació de la Reserva', styles['Heading2'])],
        ['Número de reserva:', str(reservation.id)],
        ['Data d\'entrada:', reservation.entry.strftime('%d/%m/%Y')],
        ['Data de sortida:', reservation.exit.strftime('%d/%m/%Y')],
        ['Número d\'hostes:', str(reservation.num_guests)],
        ['Tipus de pensió:', reservation.pension_type],
        ['Tipus d\'habitació:', reservation.room.room_type],
        ['Número d\'habitació:', str(reservation.room.room_num)]
    ]
    reservation_table = Table(reservation_data, colWidths=[200, 260])
    reservation_table.setStyle(TableStyle([
        ('SPAN', (0, 0), (1, 0)),
        ('BACKGROUND', (0, 0), (1, 0), colors.lightgrey),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 1), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 1), (-1, -1), 0.25, colors.black),
        ('TOPPADDING', (0, 1), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
    ]))

    client_data = [
        [Paragraph('Informació del Client', styles['Heading2'])],
        ['Nom del client:', f"{client.first_name} {client.last_name}"],
        ['Document d\'identitat:', client.id_number],
        ['Correu electrònic:', client.email],
        ['Telèfon:', client.phone_number]
    ]
    client_table = Table(client_data, colWidths=[200, 260])
    client_table.setStyle(TableStyle([
        ('SPAN', (0, 0), (1, 0)),
        ('BACKGROUND', (0, 0), (1, 0), colors.lightgrey),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 1), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 1), (-1, -1), 0.25, colors.black),
        ('TOPPADDING', (0, 1), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
    ]))

    doc.title = 'Comprovant de Check-In'
    doc.author = 'Hotel Las Palmeras'
    doc.subject = 'Check-In Document for Hotel Las Palmeras'
    doc.creator = 'JointProject'
    doc.keywords = ['Hotel Las Palmeras', 'Check-In', 'Reservation', str(reservation.id)]

    elements = [header_table, Spacer(1, 20), reservation_table, Spacer(1, 20), client_table]
    doc.build(elements)

    buffer.seek(0)
    return buffer


def create_receipt_check_out(reservation, client, despeses, extra_costs):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    styles = getSampleStyleSheet()

    header_data = [[Paragraph('Comprovant de Check-Out', styles['Title'])]]
    header_table = Table(header_data, colWidths=[460])
    header_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))

    reservation_data = [
        [Paragraph('Informació de la Reserva', styles['Heading2'])],
        ['Número de reserva:', str(reservation.id)],
        ['Data d\'entrada:', reservation.entry.strftime('%d/%m/%Y')],
        ['Data de sortida:', reservation.exit.strftime('%d/%m/%Y')],
        ['Número d\'hostes:', str(reservation.num_guests)],
        ['Tipus de pensió:', reservation.pension_type],
        ['Tipus d\'habitació:', reservation.room.room_type],
        ['Número d\'habitació:', str(reservation.room.room_num)]
    ]
    reservation_table = Table(reservation_data, colWidths=[200, 260])
    reservation_table.setStyle(TableStyle([
        ('SPAN', (0, 0), (1, 0)),
        ('BACKGROUND', (0, 0), (1, 0), colors.lightgrey),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 1), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 1), (-1, -1), 0.25, colors.black),
        ('TOPPADDING', (0, 1), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
    ]))

    client_data = [
        [Paragraph('Informació del Client', styles['Heading2'])],
        ['Nom del client:', f"{client.first_name} {client.last_name}"],
        ['Document d\'identitat:', client.id_number],
        ['Correu electrònic:', client.email],
        ['Telèfon:', client.phone_number]
    ]
    client_table = Table(client_data, colWidths=[200, 260])
    client_table.setStyle(TableStyle([
        ('SPAN', (0, 0), (1, 0)),
        ('BACKGROUND', (0, 0), (1, 0), colors.lightgrey),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 1), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 1), (-1, -1), 0.25, colors.black),
        ('TOPPADDING', (0, 1), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
    ]))

    despeses_data = [
        [Paragraph('Detall de Despeses', styles['Heading2'])],
        ['Cost de la pensió:', f"{despeses.pension_costs}€"],
        ['Cost del tipus d\'habitació:', f"{despeses.room_type_costs}€"]
    ]
    despeses_table = Table(despeses_data, colWidths=[200, 260])
    despeses_table.setStyle(TableStyle([
        ('SPAN', (0, 0), (-1, 0)),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 1), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 1), (-1, -1), 0.25, colors.black),
        ('TOPPADDING', (0, 1), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
    ]))

    extra_costs_data = [[Paragraph('Costos Extres', styles['Heading2'])]]
    extra_costs_data += [
        [f"Tipus de cost extra: {cost.extra_costs_type}", f"Preu: {cost.extra_costs_price}€"] for cost in extra_costs
    ]
    if not extra_costs:
        extra_costs_data.append(['No hi ha costos extres'])
    extra_costs_table = Table(extra_costs_data, colWidths=[200, 260])
    extra_costs_table.setStyle(TableStyle([
        ('SPAN', (0, 0), (-1, 0)),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 1), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 1), (-1, -1), 0.25, colors.black),
        ('TOPPADDING', (0, 1), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
    ]))

    doc.title = 'Comprovant de Check-Out'
    doc.author = 'Hotel Las Palmeras'
    doc.subject = 'Check-Out Document for Hotel Las Palmeras'
    doc.creator = 'JointProject'
    doc.keywords = ['Hotel Las Palmeras', 'Check-Out', 'Reservation', str(reservation.id)]

    elements = [header_table, Spacer(1, 20), reservation_table, Spacer(1, 20), client_table, Spacer(1, 20), despeses_table, Spacer(1, 20), extra_costs_table]
    doc.build(elements)

    buffer.seek(0)
    return buffer
