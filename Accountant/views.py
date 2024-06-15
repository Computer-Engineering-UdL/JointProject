from django.contrib import messages
from django.shortcuts import render, redirect

from Cleaner.models import Stock
from django.db.models import Prefetch, Sum
from django.shortcuts import redirect, render

from Accountant.config import Config as c
from Reception.models import RoomReservation, ExtraCosts
from User.decorators import worker_required
from Cleaner.forms import StockForm, AddNewCleningMaterialForm


@worker_required('accountant')
def accountant_home(request):
    return render(request, 'worker/accountant/accountant_home.html')


@worker_required('accountant')
def cleaning_material(request):
    form = StockForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            material_name = form.cleaned_data.get('material')
            if material_name:
                stock = Stock.objects.filter(material__material_name__icontains=material_name, is_active=True)
            else:
                stock = Stock.objects.filter(is_active=True)

            if 'update_stock' in request.POST:
                submitted_stock_ids = set(map(int, request.POST.getlist('stock[]')))
                all_active_stocks = set(Stock.objects.filter(is_active=True).values_list('id', flat=True))

                for stock_id in all_active_stocks:
                    item = Stock.objects.get(id=stock_id)
                    item.is_available = stock_id not in submitted_stock_ids
                    item.save()
                messages.success(request, 'Stock actualitzat correctament')

                return redirect('cleaner_stock')
        else:
            stock = Stock.objects.filter(is_active=True)
    else:
        stock = Stock.objects.filter(is_active=True)

    return render(request, 'worker/accountant/cleaning_material.html', {'form': form, 'stock': stock})



@worker_required('accountant')
def add_new_cleaning_material(request):
    if request.method == 'POST':
        form = AddNewCleningMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "S'ha creat el nou material amb èxit!")
            return redirect('accountant_home')
    else:
        form = AddNewCleningMaterialForm()
    return render(request, 'worker/accountant/new_cleaning_material.html', {'form': form})

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
