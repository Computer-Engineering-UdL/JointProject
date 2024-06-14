from django.contrib import messages
from django.db.models import Prefetch, Sum
from django.shortcuts import redirect, render

from Accountant.config import Config as c
from Reception.models import RoomReservation, ExtraCosts
from User.decorators import worker_required


@worker_required('accountant')
def accountant_home(request):
    return render(request, 'worker/accountant/accountant_home.html')


@worker_required('accountant')
def cleaning_material(request):
    return render(request, 'worker/accountant/cleaning_material.html')


@worker_required('accountant')
def tourist_tax(request):
    if request.method == 'POST':
        reservations = RoomReservation.objects.filter(tourist_tax_paid=False)
        total_guests = 0
        total_reservations = reservations.count()
        for reservation in reservations:
            reservation.tourist_tax_paid = True
            total_guests += reservation.num_guests
            # Here the api should call the payment gateway
            reservation.save()
        total_tax = total_guests * c.TOURIST_TAX_PER_CLIENT

        if total_reservations == 0 or total_guests == 0:
            messages.warning(request, 'No hi ha reserves pendents de pagament')
        else:
            messages.success(request, f"S'han pagat {total_tax}€ "
                                      f"de taxa turística per {total_guests} "
                                      f"clients de {total_reservations} reserves pendents")
    return redirect('accountant_home')


@worker_required('accountant')
def billing_data(request):
    reservations = RoomReservation.objects.select_related('room').prefetch_related(
        'despeses',
        'extracosts_set'
    ).order_by('entry')

    reservation_details = []
    for reservation in reservations:
        despeses = getattr(reservation, 'despeses', None)
        extra_costs = ExtraCosts.objects.filter(room_reservation=reservation)
        total_extra_costs = extra_costs.aggregate(Sum('extra_costs_price'))['extra_costs_price__sum'] or 0

        if despeses:
            total_price = despeses.room_type_costs + despeses.pension_costs + total_extra_costs
        else:
            total_price = total_extra_costs

        reservation_details.append({
            'reservation': reservation,
            'despeses': despeses,
            'extra_costs': extra_costs,
            'total_price': total_price
        })

    return render(request, 'worker/accountant/billing_data.html', {
        'reservation_details': reservation_details
    })
