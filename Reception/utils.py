from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def create_receipt_check_in(reservation, client):
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

    return buffer


def create_receipt_check_out(reservation, client, despeses, extra_costs):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    story = []
    styles = getSampleStyleSheet()

    story.append(Paragraph("Comprovant de Check-Out", styles['Title']))

    # Informació de la reserva
    story.append(Paragraph(f"Número de reserva: {reservation.id}", styles['Normal']))
    story.append(Paragraph(f"Data d'entrada: {reservation.entry}", styles['Normal']))
    story.append(Paragraph(f"Data de sortida: {reservation.exit}", styles['Normal']))
    story.append(Paragraph(f"Número d'hostes: {reservation.num_guests}", styles['Normal']))
    story.append(Paragraph(f"Tipus de pensió: {reservation.pension_type}", styles['Normal']))
    story.append(Paragraph(f"Tipus d'habitació: {reservation.room.room_type}", styles['Normal']))
    story.append(Paragraph(f"Número d'habitació: {reservation.room.room_num}", styles['Normal']))
    story.append(Spacer(1, 12))

    # Informació de despeses
    story.append(Paragraph(f"Costs de pensió: {despeses.pension_costs}", styles['Normal']))
    story.append(Paragraph(f"Costs de tipus d'habitació: {despeses.room_type_costs}", styles['Normal']))
    story.append(Spacer(1, 12))

    # Informació de costos extra
    for extra in extra_costs:
        story.append(Paragraph(f"Tipus de cost extra: {extra.extra_costs_type}", styles['Normal']))
        story.append(Paragraph(f"Preu del cost extra: {extra.extra_costs_price}", styles['Normal']))
    story.append(Spacer(1, 12))

    # Informació del client
    story.append(Paragraph(f"Nom del client: {client.first_name} {client.last_name}", styles['Normal']))
    story.append(Paragraph(f"Document d'identitat: {client.id_number}", styles['Normal']))
    story.append(Paragraph(f"Correu electrònic: {client.email}", styles['Normal']))
    story.append(Paragraph(f"Telèfon: {client.phone_number}", styles['Normal']))
    story.append(Spacer(1, 12))

    # Final del document
    story.append(Paragraph("Gràcies per la seva estada!", styles['Normal']))

    doc.build(story)
    buffer.seek(0)

    return buffer
